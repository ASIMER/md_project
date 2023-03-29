from datetime import datetime
from time import sleep

import scrapy
from md_project.db_orm.db_mapping import session, Comments, Games
from sqlalchemy import desc, asc

class CommentsSpider(scrapy.Spider):
    name = "comments"
    custom_settings = {
            'CONCURRENT_REQUESTS': 1,
            'CONCURRENT_ITEMS': 1,
            'DOWNLOAD_DELAY': 10,
            }
    def start_requests(self):
        urls = [
                'https://www.metacritic.com/game/playstation-4/the-witcher-3-wild-hunt/user-reviews?page=0'
                ]
        for game in session.query(Games)\
                .filter(Games.visited==False)\
                .order_by(asc(Games.score)).all():
            self.logger.info("Game name: " + game.title)
            game.visited = True
            yield scrapy.Request(url=game.web_page + '/user-reviews',
                                 callback=self.parse)
            session.commit()


    def parse(self, response):
        # get page number
        page = response.url.split("=")[-1]

        self.logger.info(f'Opened page {page}')
        # iterate through games
        title = response.css('div.product_title a.hover_none h1::text').get().strip()
        platform = response.css('span.platform a::text').get()
        if not platform:
            platform = response.css('span.platform::text').get()
        platform = platform.strip()
        for game in response.css('div.review_section'):
            # get game info
            score = game.css('div.metascore_w.user::text').get()
            if score:
                score = score.strip()
            else:
                continue

            comment = game.css('span.blurb.blurb_expanded::text').get()
            if not comment:
                comment = game.css('span::text').get()
            if not comment:
                continue
            comment = comment.strip()

            author = game.css('div.name > a::text').get()
            if not author:
                author = game.css('div.name > span::text').get()
            if not author:
                continue
            author = author.strip()

            create_date = game.css('div.review_critic '
                                   '> div.date::text').get().strip()
            if not create_date:
                continue
            create_date = datetime.strptime(create_date, "%b %d, %Y")
            """self.logger.info({
                    'score': score,
                    'game': title,
                    'comment': comment,
                    'author':author,
                    'platform': platform,
                    'create_date': create_date,
                    })"""
            try:
                comment_db = Comments(
                        score=int(score),
                        com_text=comment,
                        game=title,
                        author=author,
                        create_date=create_date,
                        platform=platform)
                session.add(comment_db)
                session.commit()
            except Exception:
                self.logger.error('Error with:', comment)
            yield {
                    'score': score,
                    'game': title,
                    'comment': comment,
                    'author':author,
                    'platform': platform,
                    'create_date': create_date,
                    }
        # change pages
        next_page = response.css('span.flipper.next '
                                 'a.action::attr(href)').get()
        if next_page is not None:
            next_page = 'https://www.metacritic.com' + next_page
            yield scrapy.Request(url=next_page, callback=self.parse)
