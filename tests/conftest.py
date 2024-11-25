import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend_server.models import Base, User, Media, Follow, Tweet
from backend_server.fastapi_api import create_app
from backend_server.routes import connect_routes


def input_test_data(base, sqlalchemy_session, sqlalchemy_engine):
    base.metadata.drop_all(sqlalchemy_engine)
    base.metadata.create_all(sqlalchemy_engine)
    user1: User = User(api_key='test', name='name_one')
    user2: User = User(api_key='test2', name='name_two')
    follow_1_2: Follow = Follow(follower_id=1, following_id=2)
    sqlalchemy_session.add_all([user1, user2, follow_1_2])

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


@pytest.fixture
def engine():
    _engine = create_engine('sqlite:///test.db')
    return _engine


@pytest.fixture
def session(engine):
    _Session = sessionmaker(engine)
    return _Session()


@pytest.fixture
def app(engine, session):
    input_test_data(base=Base, sqlalchemy_session=session, sqlalchemy_engine=engine)
    _app = create_app()
    connect_routes(app=_app, my_session=session)
    return _app


@pytest.fixture
def client(app):
    _client = TestClient(app=app)
    return _client