from typing import Optional, List, Union
import sys

from fastapi import FastAPI, Response, Path, Body, Header, File
from sqlalchemy import delete
from sqlalchemy.exc import NoResultFound, MultipleResultsFound, IntegrityError

from schemas import (ResultModel, ResultTweetModel, ResultMediaModel, ResultTweetsModel,
                                    ResultErrorModel, ResultUserInfoModelOut)
from models import User, Tweet, Media, Like, Follow


def connect_routes(app: FastAPI, my_session):
    """Функция для подключения роутов к приложению"""
    @app.post('/api/tweets', status_code=201)
    def create_new_tweet(api_key: str = Header(...),
                         tweet_data: str = Body(...),
                         tweet_media_ids: Optional[List[int]] = Body(None)):
        """
        1. Создаёт запись твита и сохраняет в базу.
        Получает строку и медиафайлы. Возвращает id созданного твита.
        """
        user_id = my_session.query(User.id).filter(User.api_key == api_key).scalar()
        new_tweet = Tweet(content=tweet_data,
                          media_ids=tweet_media_ids,
                          user_id=user_id)
        my_session.add(new_tweet)
        my_session.commit()
        return ResultTweetModel(result=True, tweet_id=new_tweet.id)


    @app.post('/api/medias', status_code=201, response_model=ResultMediaModel)
    def add_new_media(file: bytes = File(...)):
        """
        2. Создаёт запись медиафайла и сохраняет в базу.
        Получает медиафайл из form-data. Возвращает id изображения
        """
        new_media = Media(file=file)
        my_session.add(new_media)
        my_session.commit()
        return ResultMediaModel(result=True, media_id=new_media.id)


    @app.get('/api/medias/{media_id}', response_class=Response)
    def get_mediafile(media_id: int = Path(...)):
        """
        2.1. Находит запись медиафайла из БД по media_id.
        Получает media_id из пути запроса. Возвращает пользователю медиафайл в байтах.
        """
        mediafile: bytes = my_session.query(Media.file).filter(Media.id == media_id).scalar()
        return Response(content=mediafile, media_type='image')


    @app.delete('/api/tweets/{tweet_id}', status_code=200, response_model=ResultModel)
    def remove_tweet(response: Response,
                     api_key: str = Header(...),
                     tweet_id: int = Path(...)):
        """
        3 Удаляет запись твита из базы. Получает id твита.
        Возвращает сообщение статуса удаления.
        """
        user_id = my_session.query(User.id).filter(User.api_key == api_key).scalar()
        try:
            deleting_tweet = my_session.query(Tweet).filter(tweet_id == Tweet.id).one()
            if deleting_tweet.user_id != user_id:
                response.status_code = 403
                raise PermissionError
        except (NoResultFound, PermissionError):
            return ResultModel(result=False)
        my_session.delete(deleting_tweet)
        my_session.commit()
        return ResultModel(result=True)


    @app.post('/api/tweets/{tweet_id}/likes', status_code=201, response_model=ResultModel)
    def like_tweet(api_key: str = Header(...),
                   tweet_id: int = Path(...)):
        """
        4.1 Создаёт запись лайка и сохраняет в базу. Получает id твита.
        Возвращает сообщение о статусе создания лайка.
        """
        user_id = my_session.query(User.id).filter(User.api_key == api_key).scalar()
        new_like = Like(tweet_id=tweet_id,
                        user_id=user_id)
        my_session.add(new_like)
        try:
            my_session.flush()
        except IntegrityError:
            my_session.rollback()
            return ResultModel(result=False)
        my_session.commit()
        return ResultModel(result=True)


    @app.delete('/api/tweets/{tweet_id}/likes')
    def remove_like_tweet(api_key: str = Header(...),
                          tweet_id: int = Path(...)):
        """
        4.2 Удаляет запись лайка из базы. Получает id твита.
        Возвращает сообщение о статусе удаления лайка.
        """
        user_id: int = my_session.query(User.id).filter(User.api_key == api_key).scalar()
        try:
            my_session.execute(delete(Like).returning(Like)
                            .filter(user_id == Like.user_id)
                            .filter(tweet_id == Like.tweet_id)).one()
        except NoResultFound:
            my_session.rollback()
            return ResultModel(result=False)
        my_session.commit()
        return ResultModel(result=True)


    @app.post('/api/users/{following_id}/follow', status_code=201, response_model=ResultModel)
    def follow_user(api_key: str = Header(...),
                    following_id: int = Path(...)):
        """
        5. Создаёт запись подписки на пользователя и сохраняет в базу.
        Получает id пользователя. Возвращает сообщение статуса создания подписки.
        """
        user_id = my_session.query(User.id).filter(User.api_key == api_key).scalar()
        new_follow = Follow(follower_id=user_id,
                            following_id=following_id)
        my_session.add(new_follow)
        try:
            my_session.flush()
        except IntegrityError:
            my_session.rollback()
            return ResultModel(result=False)
        my_session.commit()
        return ResultModel(result=True)


    @app.delete('/api/users/{following_id}/follow', response_model=ResultModel)
    def cancel_follow_user(api_key: str = Header(...),
                           following_id: int = Path(...)):
        """
        6. Удаляет запись подписки на пользователя из базы.
        Получает id пользователя. Возвращает сообщение статуса удаления подписки.
        """
        user_id: int = my_session.query(User.id).filter(User.api_key == api_key).scalar()
        try:
            my_session.execute(delete(Follow).returning(Follow)
                                          .filter(user_id == Follow.follower_id)
                                          .filter(following_id == Follow.following_id)).one()
        except NoResultFound:
            my_session.rollback()
            return ResultModel(result=False)
        my_session.commit()
        return ResultModel(result=True)


    @app.get('/api/tweets', response_model=Union[ResultTweetsModel, ResultErrorModel])
    def get_tweets_list(response: Response,
                        api_key: str = Header(...)):
        """
        7. Возвращает json со списком твитов для ленты этого пользователя из базы данных.
        В случае любой ошибки возвращает json с описанием ошибки.
        """
        try:
            user: User = my_session.query(User).filter(User.api_key == api_key).one()
            tweets: List[Tweet] = user.tweets
            return ResultTweetsModel(result=True, tweets=tweets)
        except (NoResultFound, MultipleResultsFound):
            response.status_code = 400
            exc_info = sys.exc_info()
            er_type, er_message = str(exc_info[0]), ', '.join(exc_info[1].args)
            return ResultErrorModel(
                result=False, error_type=er_type, error_message=er_message
            )


    @app.get('/api/users/me', response_model=ResultUserInfoModelOut)
    def get_my_info(api_key: str = Header(...)):
        """
        8. Возвращает из базы данных запись профиля текущего пользователя.
        Возвращает json с информацией о пользователе, подписках и подписчиках.
        """
        user: User = my_session.query(User).filter(User.api_key == api_key).one()
        return ResultUserInfoModelOut(result=True, user=user)


    @app.get('/api/users/{user_id}', response_model=ResultUserInfoModelOut)
    def get_any_user_info(user_id: int = Path(...)):
        """
        9. Возвращает из базы данных запись произвольного профиля по его id.
        Получает id пользователя. Возвращает json с информацией о пользователе, подписках и подписчиках.
        """
        user: User = my_session.query(User).filter(user_id == User.id).one()
        return ResultUserInfoModelOut(result=True, user=user)
