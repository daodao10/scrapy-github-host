# -*- coding: utf-8 -*-
import scrapy
from host.items import HostItem

class ChinazSpider(scrapy.Spider):
    name = 'Chinaz'
    allowed_domains = ['chinaz.com']
    hostitems = []
    start_urls = ['http://ip.tool.chinaz.com/']

    def start_requests(self):
        s = """
        github.com
        assets-cdn.github.com
        avatars0.githubusercontent.com
        avatars1.githubusercontent.com
        documentcloud.github.com 
        help.github.com
        nodeload.github.com
        raw.github.com
        status.github.com
        training.github.com
        github.io
        """

        for i in s.split():
            url = 'http://ip.tool.chinaz.com/' + i.strip()
            # yield scrapy.Request(url=url, callback=self.parse)
            yield scrapy.Request(url=url, callback=self.parse_to_file)

    def parse_to_file(self, response):
        eles = response.css('p.bor-b1s span.Whwtdhalf::text')
        if len(eles) > 0:
            self.hostitems.append('%s\t%s' % (eles[1].extract(), eles[0].extract()))
        else:
            print('%s: not found' % response.url.split('/')[-1])

    def parse(self, response):
        eles = response.css('p.bor-b1s span.Whwtdhalf::text')
        if len(eles) > 0:
            # self.hostitems.append('%s %s' % (eles[1].extract(), eles[0].extract()))
            item = HostItem()
            item['host'] = eles[0].extract()
            item['ip'] = eles[1].extract()
            return item
        else:
            print('%s: not found' % response.url.split('/')[-1])

    def close(self, reason):
        print('closed: %s' % reason)
        self.write_to_host()

    def write_to_host(self):
        # hostsfile = "/etc/hosts"
        hostsfile = './github-hosts.txt'
        if len(self.hostitems) > 0:
            with open(hostsfile, "r") as f:
                src_items = [i.strip() for i in f.readlines()]
                src_items.extend(self.hostitems)
            
            with open(hostsfile, "w") as f:
                f.write("\n".join(set(src_items)))
                print('saved file %s' % hostsfile)
