from scrapy.commands import ScrapyCommand
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess

from NewsSpider.spiders.XinHuaSpider import XinHuaSpider
from NewsSpider.spiders.PengPaiSpider import PengPaiSpider
from NewsSpider.spiders.ZhongXinSpider import ZhongXinSpider
from NewsSpider.spiders.FengHuangSpider import FengHuangSpider

beginTime='2018-5-3'
endTime='2018-4-2'
class Command(ScrapyCommand):
    requires_project = True

    def syntax(self):
        return '[options]'

    def short_desc(self):
        return 'Runs all of the spiders'

    def add_options(self, parser):
        ScrapyCommand.add_options(self, parser)

    def process_options(self, args, opts):
        ScrapyCommand.process_options(self, args, opts)

    def run(self, args, opts):
        settings = get_project_settings()
        one = PengPaiSpider()
        two = ZhongXinSpider()
        three=XinHuaSpider()
        four=FengHuangSpider()
        process = CrawlerProcess(settings)
        process.crawl(one,beginTime,endTime)
        process.crawl(two,beginTime,endTime)
        process.crawl(three,beginTime,endTime)
        # process.crawl(four,beginTime,endTime)
        process.start()
