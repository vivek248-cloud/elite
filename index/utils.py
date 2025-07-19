import string
import random
from django.utils.text import slugify

def generate_unique_slug(model, field_value):
    slug = slugify(field_value)
    unique_slug = slug
    num = 1

    while model.objects.filter(slug=unique_slug).exists():
        unique_slug = f'{slug}-{num}'
        num += 1

    return unique_slug
