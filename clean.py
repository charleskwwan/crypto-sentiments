# clean.py

import argparse

from config import CONFIGS
from flask import Flask
from crypto_sentiments.models import create_db
from crypto_sentiments.models import drop_db


def parse_args():
    parser = argparse.ArgumentParser(description='Clean database')
    parser.add_argument(
        'config',
        help='Configuration',
    )

    args = parser.parse_args()
    if args.config not in CONFIGS:
        parser.error('config must be dev, stage, prod, or test')

    return args


def main():
    args = parse_args()
    app = Flask(__name__)
    app.config.from_object(CONFIGS[args.config])
    create_db(app)
    drop_db()    


if __name__ == '__main__':
    main()
