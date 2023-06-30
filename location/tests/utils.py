from core import models
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
from io import BytesIO


def sample_category(name='category 1', image=None):
    if image is None:
        image = get_temporary_image()
    category = models.Category.objects.create(name=name, image=image)
    return category


def sample_site(name='site 1', url='https://www.test.com/', location='location', quality=5.0):
    category = sample_category()
    image = get_temporary_image()
    site = models.Site.objects.create(name=name, url=url, location=location, quality=quality, image=image, category=category)
    return site

def get_temporary_image(name="test_image.jpg"):
    """
    Returns a SimpleUploadedFile object that can be used as a dummy image for testing.
    """
    image_data = BytesIO()
    image = Image.new('RGB', (100, 100), 'white')
    image.save(image_data, format='png')
    image_data.seek(0)

    return SimpleUploadedFile(name, image_data.read(), content_type="image/jpeg")
