# run.py

import argparse
import re

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
        '--ip',
        help='App IP',
        default='127.0.0.1',
    )
    parser.add_argument(
        '--port',
        help='App Port',
        type=int,
        default=5000,
    )
    parser.add_argument(
        '--dropafter',
        help='Drop database tables after termination',
        action='store_true',
        default=False,
    )
    parser.add_argument(
        '--dbinput',
        help='Serialized database file; loads database from if provided',
        default=None
    )
    parser.add_argument(
        '--dboutput',
        help='File to serialize database to',
        default=None
    )

    args = parser.parse_args()
    if args.config not in CONFIGS:
        parser.error('config must be dev, stage, prod, or test')
    if re.match(r'[^,]+,[^,]+', args.classifier_file):
        args.classifier_file = tuple(args.classifier_file.split(','))

    return args


def main():
    args = parse_args()
    initialize(CONFIGS[args.config], args.classifier_file, args.dbinput)
    try:
        print('### Running server...')
        app.run(host=args.ip, use_reloader=False)
    finally:
        print('### Shutting down...')
        if not args.dropafter:
            shutdown(args.dboutput)

if __name__ == '__main__':
    main()
