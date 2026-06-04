# app/sitemaps.py

from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse

class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'weekly'

    def items(self):
        return ['index', 'aboutus', 'contact', 'treatments', 'book_appointment']

    def location(self, item):
        return reverse(item)
