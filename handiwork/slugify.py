import re
from django.template.defaultfilters import slugify


def unique_slugify(instance, value, slug_field_name='slug', queryset=None, slug_separator='-'):
    """
    Calculates and stores a unique slug of `value` for an instance.
    :param instance:
    :param value:
    :param slug_field_name: matches model field name -> slug = models.SlugField()
    :param queryset: from the model's manager -> `.all()`
    :param slug_separator:
    :return:
    """
    slug_field = instance._meta.get_field(slug_field_name)
    slug = getattr(instance, slug_field.attname)
    slug_length = slug_field.max_length

    slug = slugify(value)
    if slug_length:
        slug = slug[:slug_length]
    slug = _slug_strip(slug, slug_separator)
    original_slug = slug

    if queryset is None:
        queryset = instance.__class__.default_manager.all()
    if instance.pk:
        queryset = queryset.exclude(pk=instance.pk)

    next = 2
    while not slug or queryset.filter(**{slug_field_name: slug}):
        slug = original_slug
        end = '%s%s' % (slug_separator, next)
        if slug_length and len(slug) + len(end) > slug_length:
            slug = slug[:slug_length - len(end)]
            slug = _slug_strip(slug, slug_separator)
        slug = '%s%s' % (slug, end)
        next += 1
    setattr(instance, slug_field.attname, slug)


def _slug_strip(value, separator='-'):
    """
    Cleans up a slug by removing slug separator characters that occur at the beginning
    or end of a slug
    :param value:
    :param separator:
    :return:
    """
    separator = separator or ''
    if separator == '-' or not separator:
        re_sep = '-'
    else:
        re_sep = '(?:-|%s)' % re.escape(separator)
    if separator != re_sep:
        value = re.sub('%s+' % re_sep, separator, value)
    if separator:
        if separator != '-':
            re_sep = re.escape(separator)
        value = re.sub(r'^%s+|%s+$' % (re_sep, re_sep), '', value)
    return value
