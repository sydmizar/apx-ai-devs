# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import TakeFirst, MapCompose
from w3lib.html import replace_escape_chars, remove_tags, replace_entities


class TalenscrapperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    job_title = scrapy.Field(
        input_processor=MapCompose(
            replace_escape_chars, remove_tags, replace_entities),
        output_processor=TakeFirst()
    )
    job_location = scrapy.Field(
        input_processor=MapCompose(
            replace_escape_chars, remove_tags, replace_entities),
        output_processor=TakeFirst()
    )
    company_name = scrapy.Field(
        input_processor=MapCompose(
            replace_escape_chars, remove_tags, replace_entities),
        output_processor=TakeFirst()
    )
    job_description = scrapy.Field(
        input_processor=MapCompose(
            replace_escape_chars, remove_tags, replace_entities),
        output_processor=TakeFirst()
    )
    job_id = scrapy.Field(
        input_processor=MapCompose(
            replace_escape_chars, remove_tags, replace_entities),
        output_processor=TakeFirst()
    )
