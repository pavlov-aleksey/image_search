import hashlib
from multiprocessing import Pool
import os
import requests

import settings


class Downloader(object):
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:18.0) Gecko/20100101 Firefox/18.0',
        'Connection': 'Keep-Alive',
        'Cache-Control': 'no-cache'
    }

    def __init__(self, url, storage_root=settings.STORAGE_ROOT):
        self.url = url
        self.path = os.path.join(storage_root, hashlib.md5(self.url).hexdigest())

    def load(self):
        with open(self.path, 'r') as file_handler:
            return file_handler.read()

    def save(self, content):
        with open(self.path, 'wb') as file_handler:
            file_handler.write(content)

        return content

    def download(self):
        if os.path.exists(self.path):
            return self.load()

        try:
            response = requests.get(self.url, headers=self.HEADERS)
        except requests.exceptions.RequestException:
            return self.save('')

        if response.status_code != requests.codes.ok:
            return self.save('')

        return self.save(response.content)


def download(url):
    Downloader(url).download()


class DownloadPool(object):

    def __init__(self, urls, pool_size=settings.THREADS):
        self.urls = urls
        self.pool = Pool(pool_size)

        self.download()

    def items(self):
        for url in self.urls:
            yield Downloader(url).download()

    def download(self):
        self.pool.map(download, self.urls)
