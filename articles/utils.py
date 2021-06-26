from datetime import datetime
from os.path import splitext

from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys


def get_timestamp_path(instance, filename):
    return '%s%s' % (datetime.now().timestamp(), splitext(filename)[1])


def resize_image(self_img):
    img = Image.open(self_img)
    output = BytesIO()
    fmt = img.format.lower()

    w = img.size[0]
    h = img.size[1]

    if w > h:
        quotient = h / w
        resized = img.resize(size=(300, round(300 * quotient)))
    else:
        quotient = w / h
        resized = img.resize(size=(round(300 * quotient), 300))

    resized.save(output, format=fmt, quality=100)
    output.seek(0)
    return InMemoryUploadedFile(file=output,
                                field_name='ImageField',
                                name='%s.%s' % (self_img.name.split('.')[0], fmt),
                                content_type='image/%s' % fmt,
                                size=sys.getsizeof(output),
                                charset=None)



