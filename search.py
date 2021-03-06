import hashlib
import logging
import os
from urllib import urlencode

import requests

from downloader import Downloader, DownloadPool
from validator import ImgValidator
from parser import LinkParser, ImgParser
import settings


class GoogleSearch(object):
    URL = 'http://www.google.com/search'
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'
    }

    def __init__(self, term):
        self.term = term
        self.job_id = hashlib.md5(self.term).hexdigest()
        self.path = os.path.join(settings.STORAGE_ROOT, self.job_id)
        self.image_urls = []

        self.log('Job started')

    def log(self, message):
        logging.info('Job #%s: %s' % (self.job_id, message))

    def parse_image_urls(self, page_urls):
        for page in DownloadPool(page_urls, self.path).items():
            self.image_urls.extend(ImgParser(page).parse())

    def download(self):
        DownloadPool(self.image_urls, self.path).download()
        self.log('Downloaded %d images' % len(self.image_urls))

    def clean(self):
        successful = 0
        for filename in os.listdir(self.path):
            if not os.path.isfile(os.path.join(self.path, filename)):
                continue

            filepath = os.path.join(self.path, filename)
            with ImgValidator(filepath) as validator:
                if not validator.is_valid():
                    os.remove(filepath)
                    continue

                successful += 1
                os.rename(filepath, '%s.%s' % (filepath, validator.extension))

        self.log('Selected %d good images' % successful)

    def search(self):
        for start in range(0, settings.STEP * settings.PAGES, settings.STEP):
            url = '%s?%s' % (self.URL, urlencode({
                'q': self.term,
                'num': settings.STEP,
                'start': start,
            }))
            page = Downloader(url, self.path).download()
            self.parse_image_urls(LinkParser(page).parse())

        self.log('Parsed %d image urls' % len(self.image_urls))

        self.download()
        self.clean()
