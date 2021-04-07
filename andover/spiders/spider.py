import scrapy

from scrapy.loader import ItemLoader

from ..items import AndoverItem
from itemloaders.processors import TakeFirst


class AndoverSpider(scrapy.Spider):
	name = 'andover'
	start_urls = ['https://www.andover.bank/Resources/Our-Bank/News']

	def parse(self, response):
		post_links = response.xpath('//a[@class="readmore"]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//div[@class="article_pager"]/a/@href').getall()
		yield from response.follow_all(next_page, self.parse)

	def parse_post(self, response):
		title = response.xpath('//div[@class="article details"]/h1/text()').get()
		description = response.xpath('//div[@class="main_content"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description if '{' not in p]
		description = ' '.join(description).strip()
		date = response.xpath('//p[@class="meta_text no_margin"]/text()').get()

		item = ItemLoader(item=AndoverItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
