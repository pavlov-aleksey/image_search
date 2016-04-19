import os
from urllib import urlencode

import requests

from downloader import Downloader, DownloadPool
from validator import ImgValidator
from parser import LinkParser, ImgParser
import settings


class GoogleSearch(object):
    PAGES = 2
    STEP = 10
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
        self.image_urls = []

    def parse_image_urls(self, page_urls):
        for page in DownloadPool(page_urls).items():
            self.image_urls.extend(ImgParser(page).parse())

    def download(self):
        DownloadPool(self.image_urls).download()

    def clean(self):
        for url in self.image_urls:
            downloader = Downloader(url)
            downloader.download()

            with ImgValidator(downloader.path) as validator:
                if not validator.is_valid():
                    os.remove(downloader.path)
                    continue

                os.rename(downloader.path, '%s.%s' % (downloader.path, validator.extension))

    def search(self):
        for start in range(0, self.STEP * self.PAGES, self.STEP):
            url = '%s?%s' % (self.URL, urlencode({
                'q': self.term,
                'num': self.STEP,
                'start': start,
            }))
            page = Downloader(url).download()
            self.parse_image_urls(LinkParser(page).parse())

        self.download()
        self.clean()
