import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from ..items import UnsplashItem
from itemloaders.processors import MapCompose

class UnsplashImgSpider(CrawlSpider):
    name = "unsplash_img"
    allowed_domains = ["unsplash.com"]
    start_urls = ["https://unsplash.com"]

    #//a[contains(@href, '/t/')] - категории
    rules = (Rule(LinkExtractor(allow=r"/t/")),
             Rule(LinkExtractor(restrict_xpaths=("//figure[@itemprop='image']//a[@itemprop='contentUrl']")), callback="parse_item", follow=True),)

    def parse_item(self, response):
        loader = ItemLoader(item=UnsplashItem(), response=response)
        loader.default_input_processor = MapCompose(str.strip)
        #URL изображения, название изображения и категорию, к которой оно принадлежит
        image_url = response.xpath('//span[text()="Download free"]/parent::a/@href').get()
        loader.add_value('url', image_url)
        loader.add_xpath('name', '//h1/text()')
        loader.add_xpath('category', '//a[@class="IQzj8 eziW_"]/text()')
        loader.add_value("image_urls", image_url)

        yield loader.load_item()
