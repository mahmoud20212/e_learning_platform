from django.contrib.sitemaps import Sitemap
from .models import Course

class CourseSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return Course.objects.filter(available=True)

    def lastmod(self, obj):
        return obj.created