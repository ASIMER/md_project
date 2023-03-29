from datetime import datetime

from md_project.db_orm.db_mapping import Games, session
from csv import DictReader

with open('./scrapper/game_list.csv') as csvfile:
    reader = DictReader(csvfile)
    rows = 0

    for row in reader:
        date = datetime.strptime(
                row['release_date'],
                "%B %d, %Y")

        game_row = Games(
                web_page=row['web_page'],
                title=row['title'],
                score=row['score'],
                platform=row['platform'],
                release_date=date)
        session.add(game_row)
        rows += 1
        if not rows % 100:
            print(f'Created {rows // 100} * 100 rows')
        try:
            session.commit()
        except Exception:
            print("Error with:", game_row)

    print('All rows comitted')
