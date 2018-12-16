# -*- coding: utf-8 -*-
import scrapy
from scrapy import Spider, Request
import requests
import lxml.html
from NewsSpider.items import NewsspiderItem

keyword="博物馆"

startPage=1

URL = 'http://search.sina.com.cn/?c=news&q={q}&range=title&time=custom&stime={stime}&etime={etime}&num=10&col=1_3&source=&from=&country=&size=&a=&page={page}&pf=2132998356&ps=2130770128&dpc=1'

class PengPaiSpider(scrapy.Spider):
    name = 'PengPaiSpider'
    allowed_domains = ['xinhuanet.com']
    page=startPage
    # start_urls = [URL.format(q=keyword,stime=beginTime,etime=endTime,page=page)]
    end=False
    flag=set()
    def __init__(self, beginTime=None, endTime=None, *args, **kwargs):
        super(PengPaiSpider, self).__init__(*args, **kwargs)
        self.beginTime=beginTime
        self.endTime=endTime
        self.start_urls =['http://search.sina.com.cn/?c=news&q=%s&range=title&time=custom&stime=%s&etime=%s&num=10&col=1_3&source=&from=&country=&size=&a=&page=%s&pf=2132998356&ps=2130770128&dpc=1'%(keyword,beginTime,endTime,self.page)]
        # print(self.start_urls)
        # print(beginTime,endTime)

    def parse(self, response):
        res=response.xpath('//div[@class="result"]/div[@class="box-result clearfix"]')
        if len(res)==0:
            self.end=True
            return

        for each in res:
            title=each.xpath('div[@class="r-info r-info2"]/h2/a//text()').extract()
            title=''.join(title)
            if title=='':
                title = each.xpath('h2/a//text()').extract()
                title = ''.join(title)
                if title=='':
                    title = each.xpath('div[@class="r-info  r-info2"]/h2/a//text()').extract()
                    title=''.join(title)
            # print(title)
            if title in self.flag:
                self.end=True
                return
            self.flag.add(title)
            author='澎湃新闻'

            excerpt=each.xpath('div[@class="r-info r-info2"]/p//text()').extract()
            excerpt=''.join(excerpt)
            if excerpt=='':
                excerpt = each.xpath('div[@class="r-info  r-info2"]/p//text()').extract()
                excerpt = ''.join(excerpt)
            #print(excerpt)

            release_time=each.xpath('div[@class="r-info r-info2"]/h2//text()').extract()
            if len(release_time)==0:
                release_time = each.xpath('h2//text()').extract()
                if len(release_time)==0:
                    release_time = each.xpath('div[@class="r-info  r-info2"]/h2//text()').extract()

            temp=release_time[-1]
            release_time=temp[-20:-9]
            # print(release_time)

            url=each.xpath('div[@class="r-info r-info2"]/h2/a/@href').extract()
            url=''.join(url)
            if url=='':
                url = each.xpath('h2/a/@href').extract()
                url = ''.join(url)
                if url == '':
                    url = each.xpath('div[@class="r-info  r-info2"]/h2/a/@href').extract()
                    url = ''.join(url)
            html = requests.get(url).content
            selector = lxml.html.document_fromstring(html)
            content = selector.xpath('//div[@id="article"]//text()')
            content = ''.join(content).replace('\'', '').replace('\r','').replace('\t','').replace('\n','')

            img_url = 'http://seopic.699pic.com/photo/50045/7863.jpg_wh1200.jpg'

            item = NewsspiderItem()
            item['title'] = title
            item['author'] = author
            item['release_time'] = release_time
            item['excerpt'] = excerpt
            item['content'] = content
            item['img_url'] = img_url
            yield item

        if not self.end:
            self.page = self.page + 1
            # print(URL.format(q=keyword, stime=self.beginTime, etime=self.endTime, page=self.page))
            yield Request(URL.format(q=keyword, stime=self.beginTime, etime=self.endTime, page=self.page), self.parse,
                          dont_filter=True)



