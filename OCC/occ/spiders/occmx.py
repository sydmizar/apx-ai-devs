import scrapy
import json
import csv
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from ..items import OccItem
import locale
locale.setlocale(locale.LC_TIME, '')

class OccmxSpider(scrapy.Spider):
    name = 'occmx'
    #allowed_domains = ['www.occ.com.mx']
    #start_urls = ['http://www.occ.com.mx/']

    #name = 'OccmxSpider'

    def __init__(self, Keywords=None, *args, **kwargs):
        super(OccmxSpider, self).__init__(*args, **kwargs)
        self.allowed_domain = ['www.occ.com.mx']
        self.Keywords = Keywords
        print(self.Keywords)
        listKeywords = "-".join(Keywords.split(','))
        page = 'https://www.occ.com.mx/empleos/de-' + listKeywords + '/en-mexico/'
        self.start_urls = [page]

    rules = {
        Rule(LinkExtractor(allow=(), restrict_xpaths=('//div[@class="pagerCount-0-2-596"]/div/ul/li'))),
        Rule(LinkExtractor(allow=(), restrict_xpaths=('//div[@class="jobCardContainer"]/a')),
             callback='parse', follow=False)}

    def parse(self, response):
        occ_item = OccItem()

        occ_item['keyWords'] = self.Keywords
        occ_item['title_role'] = response.xpath('//p[@class="text-0-2-82 heading-0-2-85 highEmphasis-0-2-103 title-0-2-707"]/text()').extract_first()
        occ_item['company'] = response.xpath('//div[@class="company-0-2-712"]/span/text()').extract_first()
        occ_item['company_rate'] = response.xpath('//span[@class="flex-0-2-4 jstart-0-2-13 acenter-0-2-21 content-0-2-757"]/p/text()').extract_first()
        occ_item['salary'] = response.xpath('//div[@class="flex-0-2-4 commissions-0-2-711"]/p/text()').extract_first()
        occ_item['city'] = response.xpath('//label[@class="text-0-2-82 standard-0-2-89 highEmphasis-0-2-103 location-0-2-713"]/text()').extract_first()
        occ_item['description'] = response.xpath('//div[@id="jobbody"]/text()').extract_first()
        occ_item['date_published'] = response.xpath('//div[@class="flex-0-2-4 jbetween-0-2-16"]/p/text()').extract_first()
        occ_item['source'] = 'occ.com.mx'
        yield occ_item
        # pass
