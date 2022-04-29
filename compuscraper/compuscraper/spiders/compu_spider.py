# RESOURCES
# https://developer.mozilla.org/es/docs/Learn/HTML/Introduction_to_HTML/Document_and_website_structure


from ..items import CompuscraperItem
import scrapy
import json
import csv
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import locale
locale.setlocale(locale.LC_TIME, '')


class Compu_Spider(CrawlSpider):
    name = 'Compu_Spider'
    def __init__(self, Keywords=None, *args, **kwargs):
        super(Compu_Spider, self).__init__(*args, **kwargs)
        self.allowed_domain = ['https://www.indeed.com/']
        self.Keywords = Keywords
        print(self.Keywords)
        # listKeywords = "%20".join(Keywords.split(','))
        # page = 'https://mx.indeed.com/jobs?q=' + listKeywords
        page = "https://www.computrabajo.com.mx/trabajo-de-data"
        self.start_urls = [page]

    rules = {
        # Para cada item itera en la paginacion
        Rule(LinkExtractor(allow=(), restrict_xpaths=(
            '//nav[@class="pag_numeric"]'))),
        Rule(LinkExtractor(allow=(), restrict_xpaths=('//a[@id="self"]')),  # itera en los resultados
             callback='parse_item', follow=False)}

    def parse_item(self, response):
        compu_item = CompuscraperItem()
        compu_item['title_role'] = response.xpath(
            '//a[@class="js-o-link fc_base"]/text()').extract_first()
        compu_item['source'] = 'www.computrabajo.com.mx'
        #datefull = response.xpath('//time').extract()
        # if (compu_item['title_role'].isnull()) and (compu_item['description'].isnull()):
        #     pass
        # else:
        yield compu_item
