# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class OhausItem(Item):
	name = Field()
	applications = Field()
	display = Field()
	operation = Field()
	communication = Field()
	construction = Field()
	design = Field()
