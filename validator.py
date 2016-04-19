from PIL import Image

import settings


class ImgValidator(object):

    def __init__(self, path):
        self.image = None

        try:
            self.image = Image.open(path)
        except (ValueError, IOError):
            pass

    def is_valid(self):
        if not self.image:
            return False

        if self.image.size < (settings.MIN_WIDTH, settings.MIN_HEIGHT):
            return False

        return self.extension in settings.ALLOWED_FORMATS

    @property
    def extension(self):
        return self.image.format.lower()

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        if self.image:
            self.image.close()
