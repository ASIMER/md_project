from md_project.db_orm.db_mapping import Comments, engine
from sqlalchemy.sql.expression import func
from langdetect import detect
from multiprocessing import Pool
from sqlalchemy.orm import sessionmaker


def detect_lang(configuration):
    part, parts = configuration
    # Create session
    Session = sessionmaker(bind=engine)
    session = Session()
    # query comments
    comments = session.query(Comments) \
        .filter(Comments.lang == None) \
        .filter(func.length(Comments.com_text) >= 200).all()
    # find number of items for each part
    i_in_part = len(comments) // parts
    print("item_in_part:", i_in_part)
    # split list in parts
    comms = [
            (
                    comments[
                    i * i_in_part
                    : i * i_in_part + i_in_part
                    if i != parts - 1 else None
                    ]
            )
            for i in range(parts)
            ]
    # iterate through part items (comments)
    for comment in comms[part]:
        try:
            detected_lang = detect(comment.com_text)
        except Exception:
            continue
        if detected_lang == 'en':
            comment.eng_lang = True
        comment.lang = detected_lang
        session.commit()
    return configuration


if __name__ == '__main__':
    processes = 8
    config = [(i, processes) for i in range(processes)]

    with Pool(processes) as p:
        p.map(detect_lang, config)