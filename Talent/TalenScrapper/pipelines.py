# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


def clean_string(variable):
    return variable.replace('\n', ' ').strip().lower()

class TalenscrapperPipeline:
    def process_item(self, item, spider):
        item['job_title'] = clean_string(item['job_title'])
        item['job_location'] = clean_string(item['job_location'])
        item['company_name'] = clean_string(item['company_name'])
        item['job_description'] = clean_string(item['job_description'])
        item['job_id'] = clean_string(item['job_id'])
        return item
