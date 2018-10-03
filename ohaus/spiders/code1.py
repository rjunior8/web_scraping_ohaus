# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.http import HtmlResponse
from lxml import html
import sys
import cfscrape
import re

from ohaus.items import OhausItem

class Ohaus(CrawlSpider):
  name = "ohaus"
  allowed_domains = ["us.ohaus.com"]
  start_urls = ["https://us.ohaus.com/en-US/products-13"]

  def parse(self, response):
    site1 = html.fromstring(response.body_as_unicode())
    scraper = cfscrape.create_scraper()
    item = OhausItem()
    for href1 in site1.xpath("//div[contains(@class, 'col-sm-6')]/a//@href"):
      url1 = "https://us.ohaus.com{}".format(href1)
      body1 = scraper.get(url1).content
      resp1 = HtmlResponse(url=url1, body=body1)
      for href2 in resp1.xpath("//div[contains(@class, 'category-family-listing')]/div[contains(@class, 'container')]/div[contains(@class, 'category-family-item')]/div[contains(@class, 'col-md-9')]/div[contains(@class, 'product-content-box')]/div[contains(@class, 'family-item-links')]/div/p/a//@href").extract():
        if href2.__contains__("Comparison?id="):
          pass
        else:
          try:
            url2 = "https://us.ohaus.com{}".format(href2)
            body2 = scraper.get(url2).content
            resp2 = HtmlResponse(url=url2, body=body2)
            body3 = body2.decode("utf-8")
            s = str(body3)
            name = re.compile(r'</title><meta property="og:title" content="(.*)" /><meta property="og:type"')
            item["name"] = name.findall(s)
            applications = re.compile(r'<div class="detail-header">\r\n\s+Applications\r\n\s+</div>\r\n\s+<div class="detail-desc">\r\n\s+(.*)\r\n\s+</div>')
            item["applications"] = applications.findall(s)
            display = re.compile(r'<div class="detail-header">Display </div>\r\n\s+<div class="detail-desc">(.*)</div>')
            item["display"] = display.findall(s)
            operation = re.compile(r'<div class="detail-header">\r\n\s+Operation\r\n\s+</div>\r\n\s+<div class="detail-desc">\r\n\s+(.*)\r\n\s+</div>')
            item["operation"] = operation.findall(s)
            communication = re.compile(r'<div class="detail-header">\r\n\s+Communication\r\n\s+</div>\r\n\s+<div class="detail-desc">\r\n\r\n\s+(.*)\r\n\s+</div>')
            item["communication"] = communication.findall(s)
            construction = re.compile(r'<div class="detail-header">\r\n\s+Construction\r\n\s+</div>\r\n\s+<div class="detail-desc">\r\n\s+(.*)\r\n\s+</div>')
            item["construction"] = construction.findall(s)
            design = re.compile(r'<div class="detail-header">\r\n\s+Design Features\r\n\s+</div>\r\n\s+<div class="detail-desc">\r\n\s+(.*)\r\n\s+</div>')
            item["design"] = design.findall(s)
            yield item
          except Exception as e:
            print("\n\n{}\nError on line: {}\n\n".format(e, sys.exc_info()[-1].tb_lineno))
            continue



