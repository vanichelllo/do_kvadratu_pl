from django.conf import settings
from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import StudyMaterial


class _MainSite:
    # Карта сайту завжди з основним доменом (а не з того, що записано в адмінці «Sites»)
    domain = settings.SITE_URL.split('://', 1)[1]
    name = domain


class MainDomainSitemap(Sitemap):
    protocol = 'https'

    def get_urls(self, page=1, site=None, protocol=None):
        return super().get_urls(page=page, site=_MainSite, protocol=self.protocol)


class StaticPagesSitemap(MainDomainSitemap):
    changefreq = 'weekly'

    def items(self):
        return ['home', 'materials_list', 'booking', 'diagnostic_test', 'about', 'offer', 'privacy']

    def location(self, item):
        return reverse(item)

    def priority(self, item):
        return {'home': 1.0, 'materials_list': 0.9, 'booking': 0.8, 'diagnostic_test': 0.8}.get(item, 0.3)


class MaterialSitemap(MainDomainSitemap):
    changefreq = 'monthly'
    priority = 0.7

    def items(self):
        return StudyMaterial.objects.filter(is_published=True).only('id').order_by('id')

    def location(self, material):
        return reverse('material_detail', args=[material.pk])
