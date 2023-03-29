import scrapy

class GameListSpider(scrapy.Spider):
    name = 'GameListSpider'
    start_urls = [
            'https://www.metacritic.com/browse/games/score/userscore/all/all/'
            'filtered?sort=desc'
          ]

    def parse(self, response):
        for title in response.css('.oxy-post-title'):
            yield {'title': title.css('::text').get()

        for next_page in response.css('a.next'):
            yield response.follow(next_page, self.parse)

