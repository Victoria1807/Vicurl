from django.conf import settings
from django.db import models

#from django.core.urlresolvers import reverse
from django_hosts.resolvers import reverse

from .validators import validate_url, validate_dot_com
from .utils import code_generator, create_shortcode

# Create your models here.

SHORTCODE_MAX = getattr(settings, "SHORTCODE_MAX", 15)

class ShortURLManager(models.Manager):
    def all(self, *args, **kwargs):
        qs_main = super(ShortURLManager, self).all(*args, **kwargs)
        qs = qs_main.filter(active=True)  # only objects with active field
        return qs

    def refresh_shortcodes(self, items=None):  # rewriting shortcodes
        qs = ShortURL.objects.filter(id__gte=1)
        if items is not None and isinstance(items, int):  # items - count of rewriting objects
            qs = qs.order_by('-id')[:items]
        new_codes = 0
        for q in qs:
            q.shortcode = create_shortcode(q)
            q.save()
            new_codes += 1
        return "New codes made: {i}".format(i=new_codes)

class ShortURL(models.Model):
    url = models.CharField(
        max_length=220,
        validators=[validate_url, validate_dot_com])
    shortcode = models.CharField(
        max_length=SHORTCODE_MAX,
        unique=True,
        blank=True)
    updated = models.DateTimeField(
        auto_now=True)
    timestamp = models.DateTimeField(
        auto_now_add=True)
    active = models.BooleanField(default=True)
    objects = ShortURLManager()

    def save(self, *args, **kwargs):
        if self.shortcode is None or self.shortcode == '':
            self.shortcode = create_shortcode(self)
        if not "http" in self.url:
            self.url = "http://" + self.url
        super(ShortURL, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.url)

    def get_short_url(self):
        url_path = reverse("scode", kwargs={"shortcode": self.shortcode}, host="www", scheme="http")
        return url_path