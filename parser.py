from pyquery import PyQuery as pq
from urlparse import urljoin


class ImgParser(object):

    def __init__(self, content, root=None):
        self.root = root
        self.content = content

    def img_url(self, url):
        if not self.root or url.startswith('http'):
            return url

        return urljoin(self.root, url)

    def parse(self):
        if not self.content:
            return []

        dom_tree = pq(self.content)

        items = []
        for item in dom_tree.find('img'):
            src = pq(item).attr('src')
            if not src:
                continue

            items.append(self.img_url(src))

        return items


class LinkParser(object):

    def __init__(self, content, root=None):
        self.root = root
        self.content = content

    def parse(self):
        if not self.content:
            return []

        dom_tree = pq(self.content)

        items = []
        for item in dom_tree.find('h3' '.r'):
            link = pq(item).find('a').attr('href')
            if link:
                items.append(link)

        return items
