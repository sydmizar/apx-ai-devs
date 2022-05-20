from scrapy import Spider, Request
from scrapy.loader import ItemLoader
from scrapy.selector import Selector
from TalenScrapper.items import TalenscrapperItem
from selenium import webdriver


class TalentSpider(Spider):
    name = 'talent'
    allowed_domains = ['mx.talent.com']

    def start_requests(self):
        self.driver = webdriver.Edge('TalenScrapper/spiders/msedgedriver.exe')
        url = "https://mx.talent.com/jobs"
        params = ['k', 'radius']
        term = getattr(self, 'term', None)
        if term:
            url = url + '?k=' + term.replace(' ', '+').lower() + '&radius=100'
        self.driver.get(url)
        yield Request(url, self.parse)

    def parse(self, response):
        cards = self.driver.find_elements_by_css_selector('.card__job')

        for card in cards:
            cardInfo = self.parse_job(card)
            l = ItemLoader(
                item=TalenscrapperItem(),
                response=response)
            l.add_value('job_title', cardInfo['job_title'])
            l.add_value('job_location', cardInfo['job_location'])
            l.add_value('company_name', cardInfo['company_name'])
            l.add_value('job_description', cardInfo['job_description'])
            l.add_value('job_id', cardInfo['job_id'])
            yield l.load_item()

        pagination_link = self.driver.find_element_by_css_selector('.pagination .page-next')
        
        if pagination_link:
            pagination_link.click()
            yield Request(self.driver.current_url, self.parse)


    def parse_job(self, card):
        card.click()
        sel = Selector(text=self.driver.page_source)
        job_id = card.get_attribute('data-id')
        cardScrapy = sel.css(f'.card__job[data-id="{job_id}"]')
        job_title = cardScrapy.css(
            '.card__job-title .card__job-link::text').get()
        job_location = cardScrapy.css(
            '.card__job-info  .card__job-location').get()
        job_location = job_location if job_location else 'N/A'

        company_name = cardScrapy.css(
            '.card__job-info .card__job-empname-label::text').get()
        job_description = sel.css(
            '.jobsPreview .jobPreview__body--description').get()
        return {
            'job_title': job_title, 'job_location': job_location,
            'company_name': company_name, 'job_description': job_description,
            'job_id': job_id
        }
