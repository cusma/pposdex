import csv
import logging
from collections.abc import Callable
from pathlib import Path

import matplotlib.pyplot as plt
import msgpack
import pytest
from fakes import FakeAlgod, FakeIndexer

from pposdex.cli import (
    DEFAULT_ALGO_THRESHOLD,
    DEFAULT_PUBLISHER,
    DEFAULT_START_BLOCK,
    build_parser,
    main,
)
from pposdex.helpers import ENV_MNEMONIC, Json
from pposdex.networks import LOCALNET, MAINNET, TESTNET, Network
from pposdex.ppos_dex_data import PPoSDexData


def test_defaults() -> None:
    args = build_parser().parse_args(["timeseries"])
    assert args.command == "timeseries"
    assert args.algo_threshold == DEFAULT_ALGO_THRESHOLD
    assert args.publisher == DEFAULT_PUBLISHER
    assert args.start_block == DEFAULT_START_BLOCK
    assert args.end_block is None
    assert not args.localhost
    assert not args.test
    assert not args.save


def test_options() -> None:
    args = build_parser().parse_args(
        ["export", "-p", "ADDR", "-a", "10", "-s", "1", "-e", "2", "--test"]
    )
    assert (args.publisher, args.algo_threshold) == ("ADDR", 10)
    assert (args.start_block, args.end_block) == (1, 2)
    assert args.test


def test_networks_are_exclusive() -> None:
    with pytest.raises(SystemExit):
        build_parser().parse_args(["health", "--localhost", "--test"])


@pytest.mark.parametrize("command", ["publish", "health"])
def test_save_only_for_plots(command: str) -> None:
    with pytest.raises(SystemExit):
        build_parser().parse_args([command, "--save"])


def test_end_block_after_start_block() -> None:
    with pytest.raises(SystemExit):
        main(["timeseries", "-s", "10", "-e", "5"])


def test_no_command_prints_help(capsys: pytest.CaptureFixture[str]) -> None:
    main([])
    assert "usage: pposdex" in capsys.readouterr().out


@pytest.mark.parametrize(
    ("flags", "level"),
    [([], logging.WARNING), (["-v"], logging.DEBUG), (["--quiet"], logging.ERROR)],
)
def test_verbosity(flags: list[str], level: int) -> None:
    assert build_parser().parse_args(["health", *flags]).log_level == level


def test_verbosity_is_exclusive() -> None:
    with pytest.raises(SystemExit):
        build_parser().parse_args(["health", "-v", "-q"])


class TestCommands:
    @pytest.fixture
    def network(
        self,
        monkeypatch: pytest.MonkeyPatch,
        algod: FakeAlgod,
        indexer: FakeIndexer,
        make_holders: Callable[[int], list[Json]],
        make_data_point: Callable[..., PPoSDexData],
    ) -> list[Network]:
        """Serve the CLI from fake clients, recording the selected networks"""
        selected: list[Network] = []

        def algod_client(network: Network) -> FakeAlgod:
            selected.append(network)
            return algod

        monkeypatch.setattr("pposdex.cli.get_algod_client", algod_client)
        monkeypatch.setattr("pposdex.cli.get_indexer_client", lambda _: indexer)
        indexer.holders = make_holders(300)
        indexer.notes[DEFAULT_PUBLISHER] = [
            msgpack.packb(make_data_point(timestamp=f"2026-11-0{day} 00:00:00.0"))
            for day in (3, 2, 1)
        ] + [b"noise"]
        return selected

    @pytest.mark.parametrize(
        ("flags", "expected"),
        [([], MAINNET), (["--test"], TESTNET), (["--localhost"], LOCALNET)],
        ids=["mainnet", "testnet", "localnet"],
    )
    def test_health(
        self,
        network: list[Network],
        flags: list[str],
        expected: Network,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        main(["health", *flags])
        out = capsys.readouterr().out
        assert "Algod Status" in out
        assert "'last-round': 1000" in out
        assert "'db-available': True" in out
        assert network == [expected]

    def test_export(
        self,
        network: list[Network],
        images: Path,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        main(["export"])
        with Path("ppos_dex_data.csv").open(encoding="utf8") as f:
            rows = list(csv.DictReader(f))
        assert [row["timestamp"][:10] for row in rows] == [
            "2026-11-03",
            "2026-11-02",
            "2026-11-01",
        ]
        assert "Exporting PPoS Dex data" in capsys.readouterr().out

    @pytest.mark.parametrize("command", ["timeseries", "snapshot"])
    def test_plots(self, network: list[Network], images: Path, command: str) -> None:
        main([command, "--save"])
        assert list((images / command).glob("*.svg"))

    @pytest.mark.parametrize("command", ["timeseries", "snapshot"])
    def test_plots_shown(
        self,
        network: list[Network],
        images: Path,
        command: str,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        shown: list[None] = []
        monkeypatch.setattr(plt, "show", lambda: shown.append(None))
        main([command])
        assert shown
        assert not list(images.rglob("*.svg"))

    def test_publish(
        self,
        network: list[Network],
        algod: FakeAlgod,
        monkeypatch: pytest.MonkeyPatch,
        publisher_mnemonic: str,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        monkeypatch.setenv(ENV_MNEMONIC, publisher_mnemonic)
        main(["publish"])
        assert "PPoS Dex published data" in capsys.readouterr().out
        assert len(algod.sent) == 1

    @pytest.mark.parametrize(
        ("argv", "error"),
        [
            (["publish"], "Mnemonic environment variable not set: ALGO_MNEMONIC"),
            (["export", "-p", "NOBODY"], "No published note found for account NOBODY."),
            (["export", "-a", "1"], "No valid PPoS Dex data published by"),
        ],
        ids=["no_mnemonic", "no_notes", "no_valid_data"],
    )
    def test_errors(
        self,
        network: list[Network],
        monkeypatch: pytest.MonkeyPatch,
        capsys: pytest.CaptureFixture[str],
        argv: list[str],
        error: str,
    ) -> None:
        monkeypatch.delenv(ENV_MNEMONIC, raising=False)
        with pytest.raises(SystemExit) as exit_:
            main(argv)
        assert exit_.value.code == 1
        assert capsys.readouterr().err.startswith(error)

    @pytest.mark.parametrize(
        ("flags", "logged"),
        [([], False), (["--verbose"], True), (["--quiet"], False)],
        ids=["default", "verbose", "quiet"],
    )
    def test_verbosity(
        self,
        network: list[Network],
        images: Path,
        capsys: pytest.CaptureFixture[str],
        flags: list[str],
        logged: bool,
    ) -> None:
        main(["export", *flags])
        main(["export", *flags])
        # Logging is set up once per run, not stacked across runs
        err = capsys.readouterr().err
        assert err.count("Skipping note") == (2 if logged else 0)
