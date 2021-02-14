"""
Usage:
  ppos_dex.py publish <api-token> <publisher-mnemonic> [--local-host]
                      [--algod-address=<ca>] [--indexer-address=<ia>]
                      [--algo-threshold=<at>]
  ppos_dex.py plot <api-token> [--local-host] [--indexer-address=<ia>]
                   [--data-address=<da>] [--algo-threshold=<at>]
                   [--starting-block=<sb>] [--ending-block=<eb>]
  ppos_dex.py snapshot <api-token> [--local-host] [--indexer-address=<ia>]
                       [--data-address=<da>] [--algo-threshold=<at>]
                       [--starting-block=<sb>]
  ppos_dex.py export <api-token> [--local-host] [--indexer-address=<ia>]
                     [--data-address=<da>] [--algo-threshold=<at>]
                     [--starting-block=<sb>] [--ending-block=<eb>]
  ppos_dex.py [--help]

Commands:
  publish   Contribute publishing PPoS Decentralization Index data on chain.
  plot      Plots PPoS Decentralization Index evolution over time.
  snapshot  Plots latest PPoS Decentralization Index data.
  export    Exports PPoS Decentralization Index data to csv.

Options:
  --local-host                      Use your Algorand Node (default: PureStake)

  -c <ca> --algod-address=<ca>      Algod Client address
        [default: https://mainnet-algorand.api.purestake.io/ps2].
  -i <ia> --indexer-address=<ia>    Indexer Client address
        [default: https://mainnet-algorand.api.purestake.io/idx2].
  -t <at> --algo-threshold=<ta>     Algo minimum balance to query
        [default: 1000].
  -a <da> --data-address=<da>       Algorand address data source
        [default: WIPE4JSUWLXKZZK6GJ6VI32PX6ZWPKBRH5YFRJCHWOVC73P5RI4DGUQUWQ].
  -s <sb> --starting-block=<sb>     Data starting block (int)
        [default: 11283636].
  -e <eb> --ending-block=<eb>       Data ending block (int)

  -h --help
"""


import sys
import csv
from docopt import docopt
from ppos_dex_data import *
from ppos_dex_plots import *
from algosdk.v2client import algod
from algosdk.v2client import indexer


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
        sys.argv.append('--help')

    args = docopt(__doc__)

    token = args['<api-token>']
    if args['--local-host']:
        purestake_token = None
    else:
        purestake_token = {'X-Api-key': token}
    publisher_mnemonic = args['<publisher-mnemonic>']
    algod_address = args['--algod-address']
    indexer_address = args['--indexer-address']
    data_address = args['--data-address']
    algo_threshold = int(args['--algo-threshold'])
    starting_block = int(args['--starting-block'])
    if args['--ending-block']:
        ending_block = int(args['--ending-block'])
        try:
            assert int(args['--starting-block']) < ending_block
        except AssertionError:
            raise AssertionError("--ending-block must be grater than "
                                 "--starting-block.")
    else:
        ending_block = args['--ending-block']

    algod_client = algod.AlgodClient(
        algod_token=token, algod_address=algod_address,
        headers=purestake_token)

    indexer_client = indexer.IndexerClient(
        indexer_token=token, indexer_address=indexer_address,
        headers=purestake_token)

    if args['publish']:
        post_ppos_dex_data(
            algod_client, indexer_client, publisher_mnemonic, algo_threshold)

    elif args['plot']:
        ppos_dex_data = get_ppos_dex_data(
            indexer_client, data_address, algo_threshold, starting_block,
            ending_block)

        timeseries_plot(ppos_dex_data)

    elif args['snapshot']:
        ppos_dex_data = get_ppos_dex_data(
            indexer_client, data_address, algo_threshold, starting_block)

        snapshot_plot(ppos_dex_data)

    elif args['export']:
        ppos_dex_data = get_ppos_dex_data(
            indexer_client, data_address, algo_threshold, starting_block,
            ending_block)

        with open('ppos_dex_data.csv', 'w', encoding='utf8',
                  newline='') as out_file:
            fc = csv.DictWriter(out_file, fieldnames=ppos_dex_data[0].keys())
            fc.writeheader()
            fc.writerows(ppos_dex_data)

    else:
        print("\nError: read ppos_dex '--help'!\n")


if __name__ == "__main__":
    main()
