from md_project.db_orm.db_mapping import Comments, session
from sqlalchemy.sql.expression import func
from langdetect import detect
from multiprocessing import Pool


def detect_lang(Comment_obj):
    try:
        detected_lang = detect(Comment_obj.com_text)
    except Exception:
        return
    if detected_lang == 'en':
        Comment_obj.eng_lang = True
    Comment_obj.lang = detected_lang
    session.commit()

rows = 0
for comment in session.query(Comments)\
        .filter(Comments.lang == None)\
        .filter(func.length(Comments.com_text) >= 200).all():


    try:
        detected_lang = detect(comment.com_text)
    except Exception:
        continue
    if detected_lang == 'en':
        comment.eng_lang = True
    comment.lang = detected_lang
    session.commit()
    rows += 1
    if not rows % 100:
        print(f'Detected {rows // 100} * 100 rows')