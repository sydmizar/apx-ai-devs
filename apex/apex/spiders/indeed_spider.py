##RESOURCES
#https://developer.mozilla.org/es/docs/Learn/HTML/Introduction_to_HTML/Document_and_website_structure


import scrapy
import json
import csv
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import locale
locale.setlocale(locale.LC_TIME, '')
from ..items import IndeedItem
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError


class Indeed_Spider(CrawlSpider):
    name = 'Indeed_spider'
    def __init__(self, Keywords=None, *args, **kwargs):
        super(Indeed_Spider, self).__init__(*args, **kwargs)
        self.allowed_domain = ['https://www.indeed.com/']
        self.Keywords = Keywords
        print(self.Keywords)
        listKeywords = "%20".join(Keywords.split(','))
        page = 'https://mx.indeed.com/jobs?q=' + listKeywords
        self.start_urls = [page]
        
    rules = {
        # Para cada item
        Rule(LinkExtractor(allow = (), restrict_xpaths = ('//div[@class="pagination"]'))), #itera en la paginacion pagination
        Rule(LinkExtractor(allow =(), restrict_xpaths = ('//div[@id="mosaic-provider-jobcards"]/a')), #itera en los resultados
                            callback = 'parse_item', follow = False, process_request='errback_web')}
    

    
    def parse_item(self, response):
        indeed_item = IndeedItem()

        indeed_item['keyWords'] = self.Keywords
        indeed_item['title_role'] = response.xpath('//h2[@class="jobTitle"]/span/text()').extract_first()
        indeed_item['company'] = response.xpath('//span[@class="companyName"]/text()').extract_first()
        indeed_item['company_rate'] = response.xpath('//span[@class="ratingNumber"]/span/text()').extract_first()
        indeed_item['salary'] = response.xpath('//div[@class="attribute_snippet"]/text()').extract_first()
        indeed_item['city'] = response.xpath('//div[@class="companyLocation"]/text()').extract_first()
        indeed_item['description'] = response.xpath('//div[@class="jobsearch-JobDescriptionText"]/text()').extract_first() #jobsearch-JobDescriptionText
        indeed_item['date_published'] = response.xpath('//span[@class="date"]/text()').extract_first()
        indeed_item['source'] = 'Indeed.com'
        #datefull = response.xpath('//time').extract()
        # if (indeed_item['title_role'].isnull()) and (indeed_item['description'].isnull()):
        #     pass
        # else:
        yield indeed_item

    def errback_web(self, failure):
        # log all failures
        self.logger.error(repr(failure))

        # in case you want to do something special for some errors,
        # you may need the failure's type:

        if failure.check(HttpError):
            # these exceptions come from HttpError spider middleware
            # you can get the non-200 response
            response = failure.value.response
            self.logger.error('HttpError on %s', response.url)

        elif failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            self.logger.error('DNSLookupError on %s', request.url)

        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.logger.error('TimeoutError on %s', request.url)


