import os


BASE_DIR = os.path.dirname(__file__)

STORAGE_ROOT = os.path.join(BASE_DIR, 'storage')

THREADS = 5

MIN_WIDTH = 100
MIN_HEIGHT = 100

ALLOWED_FORMATS = (
    'jpeg',
    'gif',
    'png',
    'bmp',
)

PAGES = 2  # Number of search pages to parse
STEP = 10  # Number of results on a search page
