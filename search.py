from urllib import urlencode

import requests

from downloader import Downloader, DownloadPool
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

    def download(self, urls):
        for page in DownloadPool(urls).items():
            DownloadPool(ImgParser(page).parse()).download()

    def search(self):
        for start in range(0, self.STEP * self.PAGES, self.STEP):
            url = '%s?%s' % (self.URL, urlencode({
                'q': self.term,
                'num': self.STEP,
                'start': start,
            }))
            page = Downloader(url).download()
            self.download(LinkParser(page).parse())
