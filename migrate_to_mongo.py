from md_project.db_orm.db_mapping import Comments, session
import datetime
from pymongo import MongoClient
client = MongoClient("mongodb+srv://asimer:253161977@md-project.k24kb."
                             "mongodb.net/MD-Project?retryWrites=true&w=majority")
db = client['md_database']
comments_col = db['comments']
rows = 0

for comment in session.query(Comments).all():
    comments_col.insert_one({
            "score": comment.score,
            "com_text": comment.com_text,
            "game": comment.game,
            "author": comment.author,
            "create_date": datetime.datetime.combine(comment.create_date,
                                                     datetime.time.min),
            "platform": comment.platform,
            })
    rows += 1
    if not rows % 100:
        print(f'Created {rows // 100} * 100 rows')