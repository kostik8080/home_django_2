from django.conf import settings
from django.core.cache import cache

from catalog.models import Category


def get_cached_subjects_category():
    if settings.CACHE_ENABLED:
        key = f'subject_list'
        subject_list = cache.get(key)
        if subject_list is None:
            subject_list = Category.objects.all()
            cache.set(key, subject_list)
    else:
        subject_list = Category.objects.all()
    return subject_list
