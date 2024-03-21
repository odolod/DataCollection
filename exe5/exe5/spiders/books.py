import scrapy
import re

class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/catalogue/page-1.html"]

    def parse(self, response):
        books = response.xpath("//li [@class = 'col-xs-6 col-sm-4 col-md-3 col-lg-3']")
        next_page = response.xpath("//li [@class = 'next']/a/@href").get()
        for book in books:
            link = book.xpath(".//h3/a/@href").get()
            yield response.follow(url=link, callback=self.parse_book)
        if next_page:
            yield response.follow(url=next_page, callback=self.parse)
        pass

    def parse_book(self, response):
        book_name = response.xpath(".//h1/text()").get() 
        book_price = response.xpath(".//p [@class = 'price_color']/text()").get() 
        book_in_stock = int(re.findall(r'\b\d+\b', response.xpath(".//p/text()")[2].get())[0])
        book_descripion = response.xpath(".//p/text()")[10].get()
        yield {'name':book_name, 'price':book_price, 'in_stock':book_in_stock, 'description':book_descripion}
        pass
