from typing import cast

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import ColumnElement
from sqlalchemy.orm import Session

from backend_server.models import Follow, Like, Media, Tweet, User


@pytest.mark.parametrize(
    'route', [
        '/api/users/1', '/api/users/2', '/api/tweets',
        '/api/users/me', '/api/medias/1', '/api/medias/2'
    ]
)
def test_ok_status_code(client: TestClient, route: str) -> None:
    """Тест статус-кода 200 GET-запросов"""
    resp = client.get(route, headers={'api-key': 'test'})
    assert resp.status_code == 200


def test_create_new_tweet(client: TestClient, session: Session) -> None:
    """Тест создания нового твита"""
    tweet_json = {'tweet_data': 'some_text', 'tweet_media_ids': [1, 2]}
    resp = client.post('/api/tweets',
                       headers={'api-key': 'test'},
                       json=tweet_json)
    assert resp.status_code == 201
    assert resp.json() == {'result': True, 'tweet_id': 3}
    assert session.query(Tweet).filter(
        cast(ColumnElement[bool], 3 == Tweet.id)).first() is not None


def test_add_new_media(client: TestClient, session: Session) -> None:
    """Тест загрузки нового медиафайла"""
    file_data = b'abcdefgh'
    resp = client.post('/api/medias', data={'file': file_data})
    assert resp.status_code == 201
    assert resp.json() == {'result': True, 'media_id': 3}
    new_media = session.query(Media).filter(
        cast(ColumnElement[bool], 3 == Media.id)).first()
    assert new_media
    assert new_media.id == 3
    assert new_media.tweet_id is None


def test_get_mediafile(client: TestClient, session: Session) -> None:
    """Тест получения медиафайла"""
    resp = client.get('/api/medias/1')
    file = session.query(Media.file).filter(
        cast(ColumnElement[bool], 1 == Media.id)).scalar()
    assert resp.status_code == 200
    assert isinstance(resp.content, bytes)
    assert resp.content == file


@pytest.mark.parametrize(('api_key', 'status_code', 'result'),
                         [('test', 200, True), ('test2', 403, False),])
def test_remove_tweet(client: TestClient, session: Session, api_key: str,
                      status_code: int, result: bool) -> None:
    """Тест удаления твита пользователя"""
    resp = client.delete('/api/tweets/1', headers={'api-key': api_key})
    assert resp.status_code == status_code
    assert resp.json() == {'result': result}
    if status_code == 200:
        assert session.query(Tweet).filter(
            cast(ColumnElement[bool], 1 == Tweet.id)).first() is None


@pytest.mark.parametrize(('tweet_id', 'result'), [(1, True), (2, False)])
def test_like_tweet(client: TestClient, session: Session,
                    tweet_id: int, result: bool) -> None:
    """Тест создания нового лайка"""
    route = '/api/tweets/{}/likes'.format(tweet_id)
    resp = client.post(route, headers={'api-key': 'test'})
    assert resp.status_code == 201
    assert resp.json() == {'result': result}
    assert session.query(Like).filter(
        cast(ColumnElement[bool], tweet_id == Like.tweet_id)).filter(
        cast(ColumnElement[bool], 1 == Like.user_id)).first() is not None


@pytest.mark.parametrize(('tweet_id', 'result'), [(2, True), (1, False)])
def test_remove_like_tweet(client: TestClient, session: Session,
                           tweet_id: int, result: bool) -> None:
    """Тест удаления лайка"""
    route = '/api/tweets/{}/likes'.format(tweet_id)
    resp = client.delete(route, headers={'api-key': 'test'})
    assert resp.status_code == 200
    assert resp.json() == {'result': result}
    assert (session.query(Like).filter(
        cast(ColumnElement[bool], tweet_id == Like.tweet_id)).filter(
        cast(ColumnElement[bool], 1 == Like.user_id)).first() is None)


@pytest.mark.parametrize(('following_id', 'result'), [(1, True), (2, False)])
def test_follow_user(client: TestClient, session: Session,
                     following_id: int, result: bool) -> None:
    """Тест создания новой подписки"""
    route = '/api/users/{}/follow'.format(following_id)
    resp = client.post(route, headers={'api-key': 'test'})
    assert resp.status_code == 201
    assert resp.json() == {'result': result}
    assert session.query(Follow) \
        .filter(cast(ColumnElement[bool], 1 == Follow.follower_id)) \
        .filter(cast(ColumnElement[bool], following_id == Follow.following_id)
                ).first() is not None


@pytest.mark.parametrize(('following_id', 'result'), [(2, True), (1, False)])
def test_cancel_follow_user(client: TestClient, session: Session,
                            following_id: int, result: bool) -> None:
    """Тест удаления подписки"""
    route = '/api/users/{}/follow'.format(following_id)
    resp = client.delete(route, headers={'api-key': 'test'})
    assert resp.status_code == 200
    assert resp.json() == {'result': result}
    assert session.query(Follow).filter(
        cast(ColumnElement[bool], 1 == Follow.follower_id)).filter(
        cast(ColumnElement[bool], following_id == Follow.following_id)
    ).first() is None


@pytest.mark.parametrize(('api_key', 'status_code', 'result'),
                         [('test', 200, True), ('wrong', 400, False)])
def test_get_tweets_list(client: TestClient, session: Session, api_key: str,
                         status_code: int, result: bool) -> None:
    """Тест получения твитов пользователя"""
    resp = client.get('/api/tweets', headers={'api-key': api_key})
    assert resp.status_code == status_code
    result_json = resp.json()
    assert result_json.get('result') == result
    if status_code == 200:
        tweets_resp = result_json.get('tweets')
        tweets_db = session.query(Tweet).filter(
            cast(ColumnElement[bool], 1 != Tweet.user_id)).all()
        assert tweets_resp
        assert tweets_db
        assert len(tweets_resp) == len(tweets_db)
        assert tweets_resp[0].get('media_ids')
        assert tweets_db[0].media_ids
        assert len(tweets_resp[0].get('media_ids')
                   ) == len(tweets_db[0].media_ids)
    else:
        assert 'NoResultFound' in result_json.get('error_type')


@pytest.mark.parametrize('api_key', ['test', 'test2'])
def test_get_my_info(client: TestClient,
                     session: Session, api_key: str) -> None:
    """Тест получения профиля текущего пользователя"""
    resp = client.get('/api/users/me', headers={'api-key': api_key})
    resp_json = resp.json()
    user = session.query(User).filter(
        cast(ColumnElement[bool], api_key == User.api_key)).first()
    assert resp_json.get('result') is True
    assert resp.status_code == 200
    assert user
    if api_key == 'test':
        assert user.following
        assert len(resp_json.get('user').get('following')
                   ) == len(user.following)
    elif api_key == 'test2':
        assert user.followers
        assert len(resp_json.get('user').get('followers')
                   ) == len(user.followers)


def test_get_any_user_info(client: TestClient, session: Session) -> None:
    """Тест получения профиля любого пользователя"""
    resp = client.get('/api/users/2', headers={'api-key': 'test'})
    assert resp.status_code == 200
    result_json = resp.json()
    assert result_json.get('result') is True
    user = session.query(User).filter(
        cast(ColumnElement[bool], 2 == User.id)).one()
    if user.followers:
        assert len(result_json.get('user').get('followers')
                   ) == len(user.followers)
    if user.following:
        assert len(result_json.get('user').get('following')
                   ) == len(user.following)
