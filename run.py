# run.py

import argparse

from config import CONFIGS
from crypto_sentiments import run


def parse_args():
    parser = argparse.ArgumentParser(description='CryptoSentiments Server')
    parser.add_argument(
        '--config',
        help='Configuration',
        default='prod',
    )

    args = parser.parse_args()
    if args.config not in CONFIGS:
        parser.error('config must be dev, stage, prod, or test')

    return args


if __name__ == '__main__':
    args = parse_args()
    run(CONFIGS[args.config])
