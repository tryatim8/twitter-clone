import pytest
from backend_server.models import User, Tweet, Media, Like, Follow


@pytest.mark.parametrize('route',['/api/users/1', '/api/users/2', '/api/tweets',
                                  '/api/users/me', '/api/medias/1', '/api/medias/2'])
def test_ok_status_code(client, route):
    """Тест статус-кода 200 GET-запросов"""
    resp = client.get(route, headers={'api-key': 'test'})
    assert resp.status_code == 200


def test_create_new_tweet(client, session):
    """Тест создания нового твита"""
    tweet_json = {'tweet_data': 'some_text', 'tweet_media_ids': [1, 2]}
    resp = client.post('/api/tweets',
                       headers={'api-key': 'test'},
                       json=tweet_json)
    assert resp.status_code == 201
    assert resp.json() == {'result': True, 'tweet_id': 3}
    assert session.query(Tweet).filter(Tweet.id == 3).first() is not None


def test_add_new_media(client, session):
    """Тест загрузки нового медиафайла"""
    file_data = b'abcdefgh'
    resp = client.post('/api/medias', data={'file': file_data})
    assert resp.status_code == 201
    assert resp.json() == {'result': True, 'media_id': 3}
    new_media = session.query(Media).filter(Media.id == 3).first()
    assert new_media.id == 3
    assert new_media.tweet_id is None


def test_get_mediafile(client, session):
    """Тест получения медиафайла"""
    resp = client.get('/api/medias/1')
    file = session.query(Media.file).filter(Media.id == 1).scalar()
    assert resp.status_code == 200
    assert isinstance(resp.content, bytes)
    assert resp.content == file


@pytest.mark.parametrize(('api_key', 'status_code', 'result'),
                         [('test', 200, True), ('test2', 403, False),])
def test_remove_tweet(client, session, api_key, status_code, result):
    """Тест удаления твита пользователя"""
    resp = client.delete('/api/tweets/1', headers={'api-key': api_key})
    assert resp.status_code == status_code
    assert resp.json() == {'result': result}
    if status_code == 200:
        assert session.query(Tweet).filter(Tweet.id == 1).first() is None


@pytest.mark.parametrize(('tweet_id', 'result'), [(1, True), (2, False)])
def test_like_tweet(client, session, tweet_id, result):
    """Тест создания нового лайка"""
    route = '/api/tweets/{}/likes'.format(tweet_id)
    resp = client.post(route, headers={'api-key': 'test'})
    assert resp.status_code == 201
    assert resp.json() == {'result': result}
    assert session.query(Like).filter(Like.tweet_id == tweet_id).filter(Like.user_id == 1).first() is not None


@pytest.mark.parametrize(('tweet_id', 'result'), [(2, True), (1, False)])
def test_remove_like_tweet(client, session, tweet_id, result):
    """Тест удаления лайка"""
    route = '/api/tweets/{}/likes'.format(tweet_id)
    resp = client.delete(route, headers={'api-key': 'test'})
    assert resp.status_code == 200
    assert resp.json() == {'result': result}
    assert (session.query(Like).filter(Like.tweet_id == tweet_id)
            .filter(Like.user_id == 1).first() is None)


@pytest.mark.parametrize(('following_id', 'result'), [(1, True), (2, False)])
def test_follow_user(client, session, following_id, result):
    """Тест создания новой подписки"""
    route = '/api/users/{}/follow'.format(following_id)
    resp = client.post(route, headers={'api-key': 'test'})
    assert resp.status_code == 201
    assert resp.json() == {'result': result}
    assert (session.query(Follow).filter(Follow.follower_id == 1)
            .filter(Follow.following_id == following_id).first() is not None)


@pytest.mark.parametrize(('following_id', 'result'), [(2, True), (1, False)])
def test_follow_user(client, session, following_id, result):
    """Тест удаления подписки"""
    route = '/api/users/{}/follow'.format(following_id)
    resp = client.delete(route, headers={'api-key': 'test'})
    assert resp.status_code == 200
    assert resp.json() == {'result': result}
    assert (session.query(Follow).filter(Follow.follower_id == 1)
            .filter(Follow.following_id == following_id).first() is None)


@pytest.mark.parametrize(('api_key', 'status_code', 'result'),
                         [('test', 200, True), ('wrong', 400, False)])
def test_get_tweets_list(client, session, api_key, status_code, result):
    """Тест получения твитов пользователя"""
    resp = client.get('/api/tweets', headers={'api-key': api_key})
    assert resp.status_code == status_code
    result_json = resp.json()
    assert result_json.get('result') == result
    if status_code == 200:
        tweets = result_json.get('tweets')
        tweets_db = session.query(Tweet).filter(Tweet.user_id == 1).all()
        assert len(tweets) == len(tweets_db)
        assert len(tweets[0].get('media_ids')) == len(tweets_db[0].media_ids)
    else:
        assert 'NoResultFound' in result_json.get('error_type')


def test_get_my_info(client, session):
    """Тест получения профиля текущего пользователя"""
    resp = client.get('/api/users/me', headers={'api-key': 'test'})
    assert resp.status_code == 200
    result_json = resp.json()
    assert result_json.get('result') is True
    user = session.query(User).filter(User.id == 1).first()
    assert len(result_json.get('user').get('followers')) == len(user.followers)
    assert len(result_json.get('user').get('following')) == len(user.following)


def test_get_any_user_info(client, session):
    """Тест получения профиля любого пользователя"""
    resp = client.get('/api/users/2', headers={'api-key': 'test'})
    assert resp.status_code == 200
    result_json = resp.json()
    assert result_json.get('result') is True
    user = session.query(User).filter(User.id == 2).first()
    assert len(result_json.get('user').get('followers')) == len(user.followers)
    assert len(result_json.get('user').get('following')) == len(user.following)
