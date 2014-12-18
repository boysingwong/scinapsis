# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
	
from scrapy.contrib.djangoitem import DjangoItem
from scrapy.item import Field

from scin.models import pub_meta, pub_material_n_method, pub_figure

class pubMetaItem(DjangoItem):
	django_model = pub_meta
	pass
	
class pubMNMItem(DjangoItem):
	django_model = pub_material_n_method
	pass

class pubFigureItem(DjangoItem):
	django_model = pub_figure
	pass
	