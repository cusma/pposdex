"""
Algorand PPoS Decentralization Index.

Usage:
  ppos_dex.py publish [--algo-threshold=<a>] [--localhost | --test]
  ppos_dex.py timeseries [--publisher=<p>] [--algo-threshold=<a>] [--start-block=<s>] [--end-block=<e>] [--localhost | --test]
  ppos_dex.py snapshot [--publisher=<p>] [--algo-threshold=<a>] [--start-block=<s>] [--end-block=<e>] [--localhost | --test]
  ppos_dex.py export [--publisher=<p>] [--algo-threshold=<a>] [--start-block=<s>] [--end-block=<e>] [--localhost | --test]
  ppos_dex.py health [--localhost | --test]
  ppos_dex.py [--help]

Commands:
  publish     Publish PPoS Dex data. Requires ALGO_MNEMONIC environment variable.
  timeseries  Plot PPoS Dex timeseries.
  snapshot    Plot latest PPoS Dex data point.
  export      Export PPoS Dex data to `.csv`.
  health      Check Algod and Indexer status.

Options:
  -a, --algo-threshold=<a>  [default: 1000]
  -p, --publisher=<p>       [default: WIPE4JSUWLXKZZK6GJ6VI32PX6ZWPKBRH5YFRJCHWOVC73P5RI4DGUQUWQ]
  -s, --start-block=<s>     [default: 11476070]
  -e, --end-block=<e>
  -l, --localhost
  -t, --test
  -h, --help
"""


import csv
import sys
from docopt import docopt
from pprint import pprint
from algokit_utils.network_clients import (
    get_algod_client,
    get_default_localnet_config,
    get_algonode_config,
    get_indexer_client,
)

import src.ppos_dex_data as pposdex
import src.plots as plots
from src.helpers import get_publisher_account


def args_types(args: dict) -> dict:
    args["--algo-threshold"] = int(args["--algo-threshold"])
    args["--start-block"] = int(args["--start-block"])
    if args["--end-block"] is not None:
        args["--end-block"] = int(args["--end-block"])
    return args


def main():
    print(
        r"""
         _______  _______           ______    ______
        |_   __ \|_   __ \        .' ____ \  |_   _ `.
          | |__) | | |__) | .--.  | (___ \_|   | | `. \ .---.  _   __
          |  ___/  |  ___// .'`\ \ _.____`.    | |  | |/ /__ \[ \ [  ]
         _| |_    _| |_   | \__. || \____) |  _| |_.' /| \__., > '  <
        |_____|  |_____|   '.__.'  \______.' |______.'  '.__.'[__]`\_]

        Algorand Pure Proof of Stake Decentralization Index (by cusma)
        """
    )

    if len(sys.argv) == 1:
        # Display help if no arguments, see:
        # https://github.com/docopt/docopt/issues/420#issuecomment-405018014
        sys.argv.append("--help")

    args = args_types(docopt(__doc__))

    if args["--end-block"]:
        try:
            assert args["--end-block"] > args["--start-block"]
        except AssertionError:
            raise AssertionError("⚠️ --end-block must be grater than --start-block")

    if args["--localhost"]:
        algod_config = get_default_localnet_config("algod")
        indexer_config = get_default_localnet_config("indexer")
    elif args["--test"]:
        algod_config = get_algonode_config("testnet", "algod", "")
        indexer_config = get_algonode_config("testnet", "indexer", "")
    else:
        algod_config = get_algonode_config("mainnet", "algod", "")
        indexer_config = get_algonode_config("mainnet", "indexer", "")

    algod_client = get_algod_client(algod_config)
    indexer_client = get_indexer_client(indexer_config)

    if args["health"]:
        print("\n⛓️ Algod Status:")
        pprint(algod_client.status(), indent=4)
        print("\n📖 Indexer Status:")
        pprint(indexer_client.health(), indent=4)

    elif args["publish"]:
        publisher = get_publisher_account()
        published_data = pposdex.post_ppos_dex_data(
            algod_client=algod_client,
            indexer_client=indexer_client,
            publisher=publisher,
            algo_threshold=args["--algo-threshold"],
            wait_rounds=3,
            data_schema=pposdex.SCHEMA,
        )
        print("📈 PPoS Dex published data:")
        pprint(published_data, indent=4)

    else:
        ppos_dex_data = pposdex.get_ppos_dex_data(
            indexer_client=indexer_client,
            publisher_address=args["--publisher"],
            algo_threshold=args["--algo-threshold"],
            data_schema=pposdex.SCHEMA,
            start_block=args["--start-block"],
            end_block=args["--end-block"],
        )
        if args["timeseries"]:
            plots.timeseries(ppos_dex_data)
        elif args["snapshot"]:
            plots.snapshot(ppos_dex_data)
        elif args["export"]:
            with open("ppos_dex_data.csv", "w", encoding="utf8", newline="") as f:
                fc = csv.DictWriter(f, fieldnames=ppos_dex_data[0].keys())
                fc.writeheader()
                fc.writerows(ppos_dex_data)


if __name__ == "__main__":
    main()
