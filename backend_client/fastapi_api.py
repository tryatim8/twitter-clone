from typing import Iterable, Optional, List

from fastapi import FastAPI, Path, Body, Header, Form
from sqlalchemy import delete
import uvicorn

from backend_client.schemas import TweetModelOut, UserInfoModelOut
from backend_client.models import User, Tweet, Media, Like, Follow, Base
from backend_client.database import session, engine


app = FastAPI()


@app.post('/api/tweets', status_code=201)
def create_new_tweet(api_key: str = Header(...),
                     tweet_data: str = Body(...),
                     tweet_media_ids: Optional[Iterable[int]] = Body(None)):
    """
    1. Создаёт запись твита и сохраняет в базу.
    Получает строку и медиафайлы. Возвращает id созданного твита.
    """
    user_id = session.query(User.id).filter(User.api_key == api_key).scalar().one()
    new_tweet = Tweet(content=tweet_data,
                      attachments=tweet_media_ids,
                      user_id=user_id)
    session.add(new_tweet)
    session.commit()
    return {'result': True, 'tweet_id': new_tweet.id}


@app.post('/api/medias', status_code=201)
def add_new_media(file: bytes = Form(...)):
    """
    2. Создаёт запись медиафайла и сохраняет в базу.
    Получает медиафайл из form-data. Возвращает id изображения
    """
    new_media = Media(file=file)
    session.add(new_media)
    session.commit()
    return {'result': True, 'media_id': new_media.id}


@app.delete('/api/tweets/{tweet_id}')
def remove_tweet(api_key: str = Header(...),
                 tweet_id: int = Path(...)):
    """
    3 Удаляет запись твита из базы. Получает id твита.
    Возвращает сообщение статуса удаления.
    """
    user_id = session.query(User.id).filter(User.api_key == api_key).scalar().one()
    deleting_tweet = session.query(Tweet).filter(Tweet.id == tweet_id)
    if deleting_tweet.user_id != user_id:
        return {'result': False}, 400
    else:
        session.delete(deleting_tweet)
        return {'result': True}


@app.post('/api/tweets/{tweet_id}/likes', status_code=201)
def like_tweet(api_key: str = Header(...),
               tweet_id: int = Path(...)):
    """
    4.1 Создаёт запись лайка и сохраняет в базу. Получает id твита.
    Возвращает сообщение о статусе создания лайка.
    """
    user_id = session.query(User.id).filter(User.api_key == api_key).scalar().one()
    new_like = Like(tweet_id=tweet_id,
                    user_id=user_id)
    session.add(new_like)
    session.commit()
    return {'result': True}


@app.delete('/api/tweets/{tweet_id}/likes', status_code=201)
def like_tweet(api_key: str = Header(...),
               tweet_id: int = Path(...)):
    """
    4.2 Удаляет запись лайка из базы. Получает id твита.
    Возвращает сообщение о статусе удаления лайка.
    """
    user_id = session.query(User.id).filter(User.api_key == api_key).scalar().one()
    deleting_like = session.execute(delete(Like).returning(Like)
                                    .filter(user_id == Like.user_id)
                                    .filter(tweet_id == Like.tweet_id)).one()
    return {'result': True} if deleting_like else {'result': False}, 400


@app.post('/api/users/{following_id}/follow', status_code=201)
def follow_user(api_key: str = Header(...),
                following_id: int = Path(...)):
    """
    5. Создаёт запись подписки на пользователя и сохраняет в базу.
    Получает id пользователя. Возвращает сообщение статуса создания подписки.
    """
    user_id = session.query(User.id).filter(User.api_key == api_key).scalar().one()
    new_follow = Follow(follower_id=user_id,
                        following_id=following_id)
    session.add(new_follow)
    session.commit()
    return {'result': True}


@app.delete('/api/users/{following_id}/follow')
def cancel_follow_user(api_key: str = Header(...),
                       following_id: int = Path(...)):
    """
    6. Удаляет запись подписки на пользователя из базы.
    Получает id пользователя. Возвращает сообщение статуса удаления подписки.
    """
    user_id = session.query(User.id).filter(User.api_key == api_key).scalar().one()
    deleting_follow = session.execute(delete(Follow).returning(Follow)
                                      .filter(user_id == Follow.follower_id)
                                      .filter(following_id == Follow.following_id)).one()
    return {'result': True} if deleting_follow else {'result': False}, 400


@app.get('/api/tweets', response_model=List[TweetModelOut])
def get_tweets_list(api_key: str = Header(...)):
    """
    7. Возвращает json со списком твитов для ленты этого пользователя из базы данных.
    В случае любой ошибки возвращает json с описанием ошибки.
    """
    user: User = session.query(User).filter(User.api_key == api_key).one()
    tweets: list[Tweet] = user.tweets
    return tweets
    # return {'result': False, 'error_type': 'some error', 'error_message': 'some message'}


@app.get('/api/users/me', response_model=UserInfoModelOut)
def get_my_info(api_key: str = Header(...)):
    """
    8. Возвращает из базы данных запись профиля текущего пользователя.
    Возвращает json с информацией о пользователе, подписках и подписчиках.
    """
    user: User = session.query(User).filter(User.api_key == api_key).one()
    return user


@app.get('/api/users/{user_id}', response_model=UserInfoModelOut)
def get_any_user_info(user_id: int = Path(...)):
    """
    9. Возвращает из базы данных запись произвольного профиля по его id.
    Получает id пользователя. Возвращает json с информацией о пользователе, подписках и подписчиках.
    """
    user: User = session.query(User).get(user_id)
    return user


if __name__ == '__main__':
    uvicorn.run(app=app)
