import scrapy


class SpiderSteamItem(scrapy.Item):
    name = scrapy.Field()
    game_category = scrapy.Field()
    number_of_reviews = scrapy.Field()
    review = scrapy.Field()
    date_of_release = scrapy.Field()
    developer = scrapy.Field()
    tags = scrapy.Field()
    price = scrapy.Field()
    available_platforms = scrapy.Field()
