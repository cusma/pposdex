"""
Algorand PPoS Decentralization Index CLI
"""

import argparse
import csv
import logging
import sys
from pprint import pprint

from pposdex import plots
from pposdex import ppos_dex_data as pposdex
from pposdex.helpers import PPoSDexError, get_publisher_account
from pposdex.networks import (
    LOCALNET,
    MAINNET,
    TESTNET,
    get_algod_client,
    get_indexer_client,
)
from pposdex.ppos_dex_data import PPoSDexData

logger = logging.getLogger("pposdex")

BANNER = r"""
         _______  _______           ______    ______
        |_   __ \|_   __ \        .' ____ \  |_   _ `.
          | |__) | | |__) | .--.  | (___ \_|   | | `. \ .---.  _   __
          |  ___/  |  ___// .'`\ \ _.____`.    | |  | |/ /__ \[ \ [  ]
         _| |_    _| |_   | \__. || \____) |  _| |_.' /| \__., > '  <
        |_____|  |_____|   '.__.'  \______.' |______.'  '.__.'[__]`\_]

        Algorand Pure Proof of Stake Decentralization Index (by cusma)
        """

DEFAULT_ALGO_THRESHOLD = 1000
DEFAULT_PUBLISHER = "WIPE4JSUWLXKZZK6GJ6VI32PX6ZWPKBRH5YFRJCHWOVC73P5RI4DGUQUWQ"
DEFAULT_START_BLOCK = 11476070


def build_parser() -> argparse.ArgumentParser:
    network = argparse.ArgumentParser(add_help=False)
    network_group = network.add_mutually_exclusive_group()
    network_group.add_argument(
        "-l", "--localhost", action="store_true", help="Use AlgoKit LocalNet"
    )
    network_group.add_argument(
        "-t", "--test", action="store_true", help="Use TestNet (default: MainNet)"
    )
    verbosity = network.add_mutually_exclusive_group()
    verbosity.add_argument(
        "-v",
        "--verbose",
        dest="log_level",
        action="store_const",
        const=logging.DEBUG,
        default=logging.WARNING,
        help="Show debug details",
    )
    verbosity.add_argument(
        "-q",
        "--quiet",
        dest="log_level",
        action="store_const",
        const=logging.ERROR,
        help="Show errors only",
    )

    threshold = argparse.ArgumentParser(add_help=False)
    threshold.add_argument(
        "-a",
        "--algo-threshold",
        type=int,
        default=DEFAULT_ALGO_THRESHOLD,
        help="Minimum account balance in ALGO (default: %(default)s)",
    )

    data = argparse.ArgumentParser(add_help=False)
    data.add_argument(
        "-p",
        "--publisher",
        default=DEFAULT_PUBLISHER,
        help="PPoS Dex data publisher address (default: %(default)s)",
    )
    data.add_argument(
        "-s",
        "--start-block",
        type=int,
        default=DEFAULT_START_BLOCK,
        help="Data starting block (default: %(default)s)",
    )
    data.add_argument("-e", "--end-block", type=int, help="Data ending block")

    save = argparse.ArgumentParser(add_help=False)
    save.add_argument(
        "--save", action="store_true", help="Save plots in './docs/images'"
    )

    parser = argparse.ArgumentParser(
        prog="pposdex", description="Algorand PPoS Decentralization Index."
    )
    commands = parser.add_subparsers(dest="command", metavar="<command>")
    commands.add_parser(
        "publish",
        parents=[threshold, network],
        help="Publish PPoS Dex data. Requires ALGO_MNEMONIC environment variable.",
    )
    commands.add_parser(
        "timeseries",
        parents=[data, threshold, network, save],
        help="Plot PPoS Dex timeseries.",
    )
    commands.add_parser(
        "snapshot",
        parents=[data, threshold, network, save],
        help="Plot latest PPoS Dex data point.",
    )
    commands.add_parser(
        "export",
        parents=[data, threshold, network],
        help="Export PPoS Dex data to `.csv`.",
    )
    commands.add_parser(
        "health", parents=[network], help="Check Algod and Indexer status."
    )
    return parser


def main(argv: list[str] | None = None) -> None:
    print(BANNER)

    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command is None:
        parser.print_help()
        return

    end_block = getattr(args, "end_block", None)
    if end_block is not None and end_block <= args.start_block:
        parser.error("--end-block must be greater than --start-block")

    configure_logging(args.log_level)
    try:
        run(args)
    except PPoSDexError as err:
        logger.error("%s", err)
        sys.exit(1)


def configure_logging(level: int) -> None:
    # Diagnostics go to stderr, command results to stdout
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(message)s"))
    logger.handlers = [handler]
    logger.setLevel(level)
    logger.propagate = False


def run(args: argparse.Namespace) -> None:
    if args.localhost:
        network = LOCALNET
    elif args.test:
        network = TESTNET
    else:
        network = MAINNET

    algod_client = get_algod_client(network)
    indexer_client = get_indexer_client(network)

    if args.command == "health":
        print("\n⛓️ Algod Status:")
        pprint(algod_client.status(), indent=4)
        print("\n📖 Indexer Status:")
        pprint(indexer_client.health(), indent=4)

    elif args.command == "publish":
        publisher = get_publisher_account()
        published_data = pposdex.post_ppos_dex_data(
            algod_client=algod_client,
            indexer_client=indexer_client,
            publisher=publisher,
            algo_threshold=args.algo_threshold,
            wait_rounds=3,
        )
        print("📈 PPoS Dex published data:")
        pprint(published_data, indent=4)

    else:
        ppos_dex_data = pposdex.get_ppos_dex_data(
            indexer_client=indexer_client,
            publisher_address=args.publisher,
            algo_threshold=args.algo_threshold,
            start_block=args.start_block,
            end_block=args.end_block,
        )
        show_data(args, ppos_dex_data)


def show_data(args: argparse.Namespace, ppos_dex_data: list[PPoSDexData]) -> None:
    if args.command == "timeseries":
        if args.save:
            print("💾 Saving timeseries in './docs/images/timeseries'...\n")
        plots.timeseries(ppos_dex_data, args.save)
    elif args.command == "snapshot":
        if args.save:
            print("💾 Saving snapshots in './docs/images/snapshot'...\n")
        plots.snapshot(ppos_dex_data, args.save)
    elif args.command == "export":
        print("💾 Exporting PPoS Dex data to 'ppos_dex_data.csv'...\n")
        with open("ppos_dex_data.csv", "w", encoding="utf8", newline="") as f:
            fc = csv.DictWriter(f, fieldnames=ppos_dex_data[0].keys())
            fc.writeheader()
            fc.writerows(ppos_dex_data)


if __name__ == "__main__":
    main()
