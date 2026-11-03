import pytest

from pposdex.cli import (
    DEFAULT_ALGO_THRESHOLD,
    DEFAULT_PUBLISHER,
    DEFAULT_START_BLOCK,
    build_parser,
    main,
)


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
