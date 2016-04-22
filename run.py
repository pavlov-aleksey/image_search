import argparse
import logging
import os
import sys

from search import GoogleSearch
import settings


logging.basicConfig(stream=sys.stdout, level=logging.INFO)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('term', help='search term')

    if not os.path.exists(settings.STORAGE_ROOT):
        try:
            os.makedirs(settings.STORAGE_ROOT)
        except OSError:
            logging.error('Unable to create storage folder %s' % settings.STORAGE_ROOT)
            sys.exit(1)

    GoogleSearch(parser.parse_args().term).search()
