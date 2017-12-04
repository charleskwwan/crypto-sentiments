# run.py

import argparse

from config import CONFIGS
from crypto_sentiments import app
from crypto_sentiments import initialize
from crypto_sentiments import shutdown
from crypto_sentiments.common.sentiments.classify import TweetClassifier # required for unpickle


def parse_args():
    parser = argparse.ArgumentParser(description='CryptoSentiments Server')
    parser.add_argument(
        'classifier_file',
        help='Pickle file from which to load a pretrained classifier',
    )
    parser.add_argument(
        '--config',
        help='Configuration',
        default='prod',
    )
    parser.add_argument(
        '--dropafter',
        help='Drop database tables after termination',
        type=bool,
        default=False,
    )

    args = parser.parse_args()
    if args.config not in CONFIGS:
        parser.error('config must be dev, stage, prod, or test')

    return args


def main():
    args = parse_args()
    initialize(CONFIGS[args.config], args.classifier_file)
    try:
        print('### Running server...')
        app.run(use_reloader=False)
    finally:
        if not args.dropafter:
            shutdown()

if __name__ == '__main__':
    main()
