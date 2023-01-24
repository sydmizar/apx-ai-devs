# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class OccItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    keyWords = scrapy.Field()
    title_role = scrapy.Field()
    company = scrapy.Field()
    company_rate = scrapy.Field()
    salary = scrapy.Field()
    city = scrapy.Field()
    description = scrapy.Field()
    date_published = scrapy.Field()
    source = scrapy.Field()
    pass
