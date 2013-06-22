# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

import  json
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from scrapy.contrib.exporter import JsonItemExporter
from scrapy.exceptions import DropItem


incomingData = []
newData = []



class PersistData(object):
    def __init__(self):
        dispatcher.connect(self.spider_opened, signals.spider_opened)

    def spider_opened(self,spider):
        import os
        if os.path.exists('storage\\%s_new_items.json' % spider.name):
            os.remove('storage\\%s_new_items.json' % spider.name)


    def process_item(self,item,spider):
        incomingData.append(item)
        return  item


class CheckNewItems(object):
    def __init__(self):
        self.arr = dict()
        dispatcher.connect(self.spider_opened, signals.spider_opened)

    def spider_opened(self,spider):
        try:
            with open('storage\\%s_items.json' % spider.name,'r') as json_file:
                data = json.load(json_file)
                for el in data:
                    self.arr[el['title'][0]] = el['link'][0]
        except IOError:
            pass

    def process_item(self, item, spider):
        if self.arr.has_key(item['title'][0]):
            raise DropItem("Is not a new item: %s" % item)
        else:
            print "New item"
            return item

class SaveNewItems(object):
    def __init__(self):
        self.files = []
        dispatcher.connect(self.spider_opened, signals.spider_opened)
        dispatcher.connect(self.spider_closed, signals.spider_closed)


    def process_item(self, item, spider):
        self.new_file_exporter.export_item(item)
        print "Save " + item['title'][0]
        return item

    def spider_opened(self,spider):
        self.new_item_file =  open('storage\\%s_new_items.json' % spider.name, 'w')
        self.new_file_exporter = JsonItemExporter(self.new_item_file)
        self.new_file_exporter.start_exporting()


    def spider_closed(self, spider):
        with open('storage\\%s_items.json' % spider.name, 'w') as items_file:
            self.exporter = JsonItemExporter(items_file)
            self.exporter.start_exporting()
            for item in incomingData:
                self.exporter.export_item(item)
            self.exporter.finish_exporting()
            self.new_file_exporter.finish_exporting()
            items_file.close()
            self.new_item_file.close()
