import csv

import scrapy
from twisted.python import filepath


class CommentsListSpider(scrapy.Spider):
    name = "comments_list"

    def start_requests(self):
        games = [
                "https://www.metacritic.com/game/playstation-4/the-witcher-3-wild-hunt"
                ]
        urls = [
                game_p + '/user-reviews'
                for game_p in games
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
            title = game.css('div.product_title a h1::text').get().strip()
            comment = game.css('div.metascore_w.user::text').get().strip()
            score = game.css('div.metascore_w.user::text').get().strip()
            platform = game.css('span.platform a::text').get().strip()
            c_date = game.css('div.review_critic '
                              '> div.date::text').get().strip()
            yield {
                'number': number,
                'score': score,
                'game': title,
                'comment': comment,
                'platform': platform,
                'create_date': c_date,
                }
        # change pages
        next_page = response.css('span.flipper.next '
                                 'a.action::attr(href)').get()
        next_page = 'https://www.metacritic.com' + next_page
        if next_page is not None:
            yield scrapy.Request(url=next_page, callback=self.parse)
