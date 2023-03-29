import csv

import scrapy
from twisted.python import filepath


class GameListSpider(scrapy.Spider):
    name = "game_list"

    def start_requests(self):
        urls = [
                'https://www.metacritic.com/browse/games/score/userscore/all'
                f'/all/filtered?sort=desc&page={page_n}'
                for page_n in range(175)
                ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        page = response.url.split("=")[-1]
        self.logger.info(f'Opened page {page}')
        # iterate through games
        for game in response.css('td.clamp-summary-wrap'):
            # get game info
            number = game.css('span.title.numbered::text').get().strip()[:-1]
            title = game.css('a.title h3::text').get().strip()
            score = game.css('div.metascore_w.user::text').get().strip()
            platform = game.css('div.platform span.data::text').get().strip()
            r_date = game.css('div.clamp-details > span::text').get().strip()
            w_page = game.css('a.title::attr(href)').get().strip()
            w_page = "https://www.metacritic.com" + w_page
            yield {
                'number': number,
                'title': title,
                'score': score,
                'platform': platform,
                'release_date': r_date,
                'web_page': w_page,
                }
        # change pages
        #next_page = response.css('span.flipper.next '
        #                         'a.action::attr(href)').get()
        #next_page = 'https://www.metacritic.com' + next_page
        #if next_page is not None:
        #    yield scrapy.Request(url=next_page, callback=self.parse)
