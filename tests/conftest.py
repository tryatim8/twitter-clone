import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.orm.decl_api import DeclarativeMeta

from backend_server.database import Base
from backend_server.fastapi_api import create_app
from backend_server.models import Follow, Media, Tweet, User
from backend_server.routes import connect_routes


def input_test_data(
        base: DeclarativeMeta,
        sqlalchemy_session: Session,
        sqlalchemy_engine: Engine,
) -> None:
    """Добавляет первичные данные в БД приложения"""
    base.metadata.drop_all(sqlalchemy_engine)
    base.metadata.create_all(sqlalchemy_engine)
    user1: User = User(api_key='test', name='name_one')
    user2: User = User(api_key='test2', name='name_two')
    follow_1_2: Follow = Follow(follower_id=1, following_id=2)
    sqlalchemy_session.add_all([user1, user2, follow_1_2])

    with open('img_1.png', 'rb') as img_one:
        with open('img_1.png', 'rb') as img_two:
            media1: Media = Media(file=img_one.read())
            media2: Media = Media(file=img_two.read())
    tweet1: Tweet = Tweet(content='some_text', media_ids=[1, 2])
    tweet2: Tweet = Tweet(content='some_text2', media_ids=[2])
    tweet1.medias.extend([media1, media2])
    tweet2.medias.append(media2)
    user1.tweets.append(tweet1)
    user2.tweets.append(tweet2)
    user1.liked_tweets.append(tweet2)

    sqlalchemy_session.commit()


@pytest.fixture
def engine() -> Engine:
    """Инициализация экземпляра двигателя БД"""
    _engine = create_engine('sqlite:///test.db')
    return _engine


@pytest.fixture
def session(engine: Engine) -> Session:
    """Инициализация экземпляра объекта сессии ORM"""
    _Session = sessionmaker(engine)
    return _Session()


@pytest.fixture
def app(engine: Engine, session: Session) -> FastAPI:
    """Инициализация экземпляра приложения"""
    input_test_data(base=Base,
                    sqlalchemy_session=session,
                    sqlalchemy_engine=engine)
    _app = create_app()
    connect_routes(app=_app, my_session=session)
    return _app


@pytest.fixture
def client(app: FastAPI) -> TestClient:
    """Инициализация экземпляра тестового клиента"""
    _client = TestClient(app=app)
    return _client
