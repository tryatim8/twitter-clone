from fastapi import FastAPI
from sqlalchemy import exc
import logging

from models import User, Tweet, Media, Follow

logging.basicConfig()
logger = logging.getLogger(__name__)


def create_app():
    _app = FastAPI()
    return _app


def input_test_data(base, sqlalchemy_session, sqlalchemy_engine):
    try:
        base.metadata.create_all(sqlalchemy_engine)
        user1: User = User(api_key='test', name='name_one')
        user2: User = User(api_key='test2', name='name_two')
        follow_1_2: Follow = Follow(follower_id=1, following_id=2)
        sqlalchemy_session.add_all([user1, user2, follow_1_2])
        sqlalchemy_session.flush()

        media1: Media = Media(file=b'abcd')
        media2: Media = Media(file=b'efgh')
        tweet1: Tweet = Tweet(content='some_text', attachments=[1, 2])
        tweet2: Tweet = Tweet(content='some_text2', attachments=[2])
        tweet1.medias.extend([media1, media2])
        tweet2.medias.append(media2)
        user1.tweets.append(tweet1)
        user2.tweets.append(tweet2)
        user1.liked_tweets.append(tweet2)

        sqlalchemy_session.commit()
    except exc.IntegrityError:
        sqlalchemy_session.rollback()
        print('Test data is OK')
