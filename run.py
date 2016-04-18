import os
import sys

from search import GoogleSearch
import settings


if __name__ == '__main__':
    if not os.path.exists(settings.STORAGE_ROOT):
        try:
            os.makedirs(settings.STORAGE_ROOT)
        except OSError:
            print 'Unable to create storage folder %s' % settings.STORAGE_ROOT
            sys.exit(1)

    GoogleSearch('emotions').search()

