# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
import hashlib
from pathlib import Path
from scrapy.loader import ItemLoader


class Exe6Pipeline:
    def process_item(self, item, spider):
        return item

class UnsplashImagesPipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None, *, item=None):
        delimiter = '_'
        file_name_prefix = ''
        if item['name']:
            if isinstance(item['name'], list):
                file_name_prefix = item['name'][0]
            else:
                file_name_prefix = item['name']
            file_name_prefix = f"{''.join([symb for symb in delimiter.join(file_name_prefix.split()) if symb.isalnum() or symb == delimiter])}-"
        image_guid = hashlib.sha1(request.url.encode()).hexdigest()
        file_name = f"{file_name_prefix}{image_guid}.jpg"
        # loader = ItemLoader(item=item, response=response)
        # loader.add_value('file_name', file_name)
        item['filename'] = Path(self.store.basedir) / file_name
        # print(f'UnsplashImagesPipeline:{item=}')
        # print(f'{self.store.basedir=}')
        return file_name