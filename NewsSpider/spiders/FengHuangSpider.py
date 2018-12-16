# -*- coding: utf-8 -*-
import scrapy
import time
from scrapy import Spider, Request
from NewsSpider.items import NewsspiderItem
import requests
import lxml.html


# beginTime='2018-5-5'
# endTime='2018-5-8'
keyword="博物馆"
startPage=1
URL='http://search.ifeng.com/sofeng/article?c=1&u=&q={q}&p={p}'
# bt = int(time.mktime(time.strptime(beginTime, "%Y-%m-%d")))
# et = int(time.mktime(time.strptime(endTime, "%Y-%m-%d")))

class FengHuangSpider(scrapy.Spider):
    name = 'FengHuangSpider'
    allowed_domains = ['search.ifeng.com']
    page=startPage
    # start_urls = [URL.format(q=keyword,p=page)]
    end=False
    flag=set()
    def __init__(self, beginTime=None, endTime=None, *args, **kwargs):
        super(FengHuangSpider, self).__init__(*args, **kwargs)
        if beginTime is not None:
            self.bt=int(time.mktime(time.strptime(beginTime, "%Y-%m-%d")))
        if endTime is not None:
            self.et=int(time.mktime(time.strptime(endTime, "%Y-%m-%d")))
        self.start_urls =[URL.format(q=keyword,p=self.page)]
    def parse(self, response):
        res=response.xpath('//div[@class="mainM"]/div[@class="searchResults"]')
        # print(res)
        if len(res)==0:
            self.end=True
            return

        for each in res:
            title=each.xpath('p[@class="fz16 line24"]//text()').extract()
            title=''.join(title)
            # print(title)
            # if title in self.flag:
            #     self.end=True
            #     return
            self.flag.add(title)

            author='凤凰资讯'

            excerpt=each.xpath('p//text()').extract()
            release_time = excerpt[-1].replace('\r','').replace('\t','').replace('\n','').split()
            release_time = release_time[1]
            excerpt=excerpt[0:-1]
            excerpt=''.join(excerpt)
            # print(excerpt)
            # print(release_time)
            if release_time[0]!=2:
                release_time= time.strftime("%Y-%m-%d", time.localtime())
            # 进行时间的判断
            rtime=int(time.mktime(time.strptime(release_time, "%Y-%m-%d")))


            url=each.xpath('p[@class="fz16 line24"]/a/@href').extract()
            url=''.join(url)
            # print(url)
            html = requests.get(url).content
            selector = lxml.html.document_fromstring(html)
            content = selector.xpath('//div[@id="main_content"]//text()')
            content = ''.join(content).replace('\'', '').replace('\r','').replace('\t','').replace('\n','')
            if content=='':
                content = selector.xpath('//div[@class="article"]/p//text()')
                content=''.join(content)
            if content=='':
                content=excerpt
            # print(content)

            img_url = 'http://seopic.699pic.com/photo/50045/7863.jpg_wh1200.jpg'
            item = NewsspiderItem()
            #如果在此时间范围内,存取这个item
            if rtime>=self.bt and rtime<=self.et:
                item['title'] = title
                item['author'] = author
                item['release_time'] = release_time
                item['excerpt'] = excerpt
                item['content'] = content
                item['img_url'] = img_url
                yield item

        # print(self.end)
        if self.page!=12:
            self.page=self.page+1
            yield Request(URL.format(q=keyword,p=self.page),self.parse,dont_filter=True)





