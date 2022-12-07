import scrapy
from spider_steam.items import SpiderSteamItem


def stripper(arr):
    return [x.strip() for x in arr]


class SteamSpider(scrapy.Spider):
    name = 'SteamSpider'
    allowed_domains = ['store.steampowered.com']
    start_urls = ['https://store.steampowered.com/search/?term=monsters', 'https://store.steampowered.com/search/?term=ships', 'https://store.steampowered.com/search/?term=math']

    def start_requests(self):
        for start_url in self.start_urls:
            yield scrapy.Request(url=start_url, callback=self.site_response_parser)

    def site_response_parser(self, response):
        links = response.xpath('//@href').extract()
        for link in links:
            if '/app' in link:
                yield scrapy.Request(url=link, callback=self.game_parser)

    def game_parser(self, response):
        game = SpiderSteamItem()
        game['name'] = response.css('div.apphub_AppName::text').get()
        category = response.xpath('//div[@class="blockbg"]//text()').extract()
        good_looking_category = category[1::2][1:-1]
        game['game_category'] = good_looking_category
        pl = stripper(response.xpath('//div[@class="sysreq_tabs"]//text()').extract())
        game['available_platforms'] = [x for x in pl if x != '']
        game['number_of_reviews'] = response.css('meta[itemprop="reviewCount"]').attrib['content']
        rew = response.xpath('//div[@class="summary column"]//span[@class="game_review_summary positive"]//text()').extract()
        if len(rew) > 0:
            game['review'] = rew[0]
        game['date_of_release'] = response.css('div.date::text').get()
        game['developer'] = response.xpath('//div[@id="developers_list"]//text()').extract()[1]
        game['tags'] = stripper(response.xpath('//a[@class="app_tag"]//text()').extract())
        game['price'] = response.xpath('//div[@class="discount_original_price"]//text()').extract()[0]
        yield game
