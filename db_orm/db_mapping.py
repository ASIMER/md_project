"""
SQLAlchemy orm database mapping
"""
from uuid import uuid4

from sqlalchemy import Column, Integer, LargeBinary, String, Date, Numeric, \
    Text, Boolean
from sqlalchemy import create_engine
from os import environ
from dotenv import load_dotenv
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

# Loaf environment variables
load_dotenv()
engine = create_engine(
        f"{environ.get('DIALECT')}+{environ.get('DB_DRIVER')}://"
        f"{environ.get('MYSQL_USER')}:{environ.get('MYSQL_PASSWORD')}"
        f"@{environ.get('DB_ADRESS')}/{environ.get('DB_NAME')}"
        f"?charset=utf8mb4")

# Create session
Session = sessionmaker(bind=engine)
session = Session()

# Map tables
Base = declarative_base()


class Comments(Base):
    """
    `comments` table mapping
    """
    __tablename__ = 'comments'

    com_id = Column(LargeBinary, primary_key=True,
                    default=lambda x: uuid4().bytes)
    game = Column(String(300))
    score = Column(Integer)
    author = Column(String(150))
    create_date = Column(Date)
    platform = Column(String(50))
    com_text = Column(Text())
    eng_lang = Column(Boolean)
    lang = Column(String(9))

    def __repr__(self):
        return "<Comment(game='%s', score='%s', " \
                        "author='%s', create_date='%s', " \
                        "platform='%s', com_text='%s'," \
                        "english_lang='%s', language='%s',)>" % (
                           self.game, self.score,
                           self.author, self.create_date,
                           self.platform, self.com_text,
                           self.eng_lang, self.lang,
                )


class Games(Base):
    """
    `games` table mapping
    """
    __tablename__ = 'games'

    web_page = Column(String(300), primary_key=True)
    title = Column(String(150))
    score = Column(Numeric(2, 1))
    platform = Column(String(50))
    release_date = Column(Date)
    visited = Column(Boolean)

    def __repr__(self):
        return "<Comment(web_page='%s', title='%s', " \
               "score='%s', platform='%s', " \
               "release_date='%s', visited='%s')>" % (
                       self.web_page, self.title,
                       self.score, self.platform,
                       self.release_date, self.visited)
