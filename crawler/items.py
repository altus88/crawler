# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class CrawlerItem(Item):
    # define the fields for your item here like:
    # name = Field()
    pass

class IDPItem(Item):
    title = Field()
    link  = Field()
