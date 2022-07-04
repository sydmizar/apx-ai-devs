import scrapy
from compuscraper.items import CompuscraperItem
from scrapy.loader import ItemLoader


class TrabajoSpider(scrapy.Spider):
    name = 'trabajo'
    start_urls = ['https://www.computrabajo.com.mx/trabajo-de-data']

    def parse(self, response):
        for article in response.css('article'):
            l = ItemLoader(item = CompuscraperItem(), selector=article)
            l.add_css('name', 'a.js-o-link.fc_base')
            yield l.load_item()

        next_page = response.css('a.b_next.buildLink').attrib['data-path']
        if next_page is not None and int(response.css('a.sel::text').get()) < 2:
            yield response.follow(next_page, callback=self.parse)
