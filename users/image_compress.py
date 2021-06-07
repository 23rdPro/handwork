from io import BytesIO
from PIL import Image
from django.core.files import File


def compress(image):
    width = 300
    # width = 300, 300  # precise
    img = Image.open(image)
    width_percent = (width/float(img.size[0]))
    size = int((float(img.size[1]) * float(width_percent)))
    img_io = BytesIO()
    img = img.resize((width, size), Image.ANTIALIAS)
    img.save(img_io, 'JPEG', quality=75)
    new_image = File(img_io, name=image.name)
    return new_image
