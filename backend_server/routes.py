import sys
from typing import List, Optional, Union, cast

from fastapi import Body, FastAPI, File, Header, Path, Response
from sqlalchemy import ColumnElement, delete
from sqlalchemy.exc import IntegrityError, MultipleResultsFound, NoResultFound
from sqlalchemy.orm import Session

from backend_server.models import Follow, Like, Media, Tweet, User
from backend_server.schemas import (
    ResultErrorModel,
    ResultMediaModel,
    ResultModel,
    ResultTweetModel,
    ResultTweetsModel,
    ResultUserInfoModelOut,
)


def connect_routes_tweets_post_delete(
        app: FastAPI, my_session: Session) -> None:
    """Фабрика роутов создания и удаления твитов приложения"""

    @app.post('/api/tweets', status_code=201,
              response_model=ResultTweetModel)
    def create_new_tweet(
            api_key: str = Header(...),
            tweet_data: str = Body(...),
            tweet_media_ids: Optional[List[int]] = Body(None)
    ) -> ResultTweetModel:
        """
        Создаёт запись твита и сохраняет в базу.
        Получает строку и медиафайлы. Возвращает id созданного твита.
        """
        user_id = my_session.query(User.id).filter(
            cast(ColumnElement[bool], api_key == User.api_key)).scalar()
        new_tweet = Tweet(content=tweet_data,
                          media_ids=tweet_media_ids,
                          user_id=user_id)
        my_session.add(new_tweet)
        my_session.commit()
        return ResultTweetModel(result=True, tweet_id=new_tweet.id)

    @app.delete('/api/tweets/{tweet_id}',
                status_code=200, response_model=ResultModel)
    def remove_tweet(
            response: Response,
            api_key: str = Header(...),
            tweet_id: int = Path(...)
    ) -> ResultModel:
        """
        Удаляет запись твита из базы. Получает id твита.
        Возвращает сообщение статуса удаления.
        """
        user_id = my_session.query(User.id).filter(
            cast(ColumnElement[bool], api_key == User.api_key)).scalar()
        try:
            deleting_tweet = my_session.query(Tweet).filter(
                cast(ColumnElement[bool], tweet_id == Tweet.id)).one()
            if deleting_tweet.user_id != user_id:
                response.status_code = 403
                raise PermissionError
        except (NoResultFound, PermissionError):
            return ResultModel(result=False)
        my_session.delete(deleting_tweet)
        my_session.commit()
        return ResultModel(result=True)


def connect_routes_medias_post_get(app: FastAPI, my_session: Session) -> None:
    """Фабрика роутов создания и получения медиафайлов приложения"""

    @app.post(
        '/api/medias', status_code=201, response_model=ResultMediaModel
    )
    def add_new_media(file: bytes = File(...)) -> ResultMediaModel:
        """
        Создаёт запись медиафайла и сохраняет в базу.
        Получает медиафайл из form-data. Возвращает id изображения
        """
        new_media = Media(file=file)
        my_session.add(new_media)
        my_session.commit()
        return ResultMediaModel(result=True, media_id=new_media.id)

    @app.get('/api/medias/{media_id}', response_class=Response)
    def get_mediafile(media_id: int = Path(...)) -> Response:
        """
        Находит запись медиафайла из БД по media_id.
        Получает media_id из пути запроса.
        Возвращает пользователю медиафайл в байтах.
        """
        mediafile: bytes = my_session.query(Media.file).filter(
            cast(ColumnElement[bool], media_id == Media.id)).scalar()
        return Response(content=mediafile, media_type='image/png')


def connect_routes_likes_post(app: FastAPI, my_session: Session) -> None:
    """Фабрика роута создания лайков"""

    @app.post('/api/tweets/{tweet_id}/likes',
              status_code=201, response_model=ResultModel)
    def like_tweet(
            api_key: str = Header(...), tweet_id: int = Path(...)
    ) -> ResultModel:
        """
        Создаёт запись лайка и сохраняет в базу. Получает id твита.
        Возвращает сообщение о статусе создания лайка.
        """
        user_id = my_session.query(User.id).filter(
            cast(ColumnElement[bool], api_key == User.api_key)).scalar()
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


def connect_routes_likes_delete(app: FastAPI, my_session: Session) -> None:
    """Фабрика роута удаления лайков"""

    @app.delete('/api/tweets/{tweet_id}/likes')
    def remove_like_tweet(
            api_key: str = Header(...), tweet_id: int = Path(...)
    ) -> ResultModel:
        """
        Удаляет запись лайка из базы. Получает id твита.
        Возвращает сообщение о статусе удаления лайка.
        """
        user_id: int = my_session.query(User.id).filter(
            cast(ColumnElement[bool], api_key == User.api_key)).scalar()
        try:
            my_session.execute(
                delete(Like).returning(Like)
                .filter(cast(ColumnElement[bool], user_id == Like.user_id))
                .filter(cast(ColumnElement[bool], tweet_id == Like.tweet_id))
            ).one()
        except NoResultFound:
            my_session.rollback()
            return ResultModel(result=False)
        my_session.commit()
        return ResultModel(result=True)


def connect_routes_follows_post(app: FastAPI, my_session: Session) -> None:
    """Фабрика роута создания подписки"""

    @app.post('/api/users/{following_id}/follow',
              status_code=201, response_model=ResultModel)
    def follow_user(
            api_key: str = Header(...), following_id: int = Path(...)
    ) -> ResultModel:
        """
        Создаёт запись подписки на пользователя и сохраняет в базу.
        Получает id пользователя.
        Возвращает сообщение статуса создания подписки.
        """
        user_id = my_session.query(User.id).filter(
            cast(ColumnElement[bool], api_key == User.api_key)).scalar()
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


def connect_routes_follows_delete(app: FastAPI, my_session: Session) -> None:
    """Фабрика роута удаления подписки"""

    @app.delete('/api/users/{following_id}/follow',
                response_model=ResultModel)
    def cancel_follow_user(
            api_key: str = Header(...), following_id: int = Path(...)
    ) -> ResultModel:
        """
        Удаляет запись подписки на пользователя из базы.
        Получает id пользователя.
        Возвращает сообщение статуса удаления подписки.
        """
        user_id: int = my_session.query(User.id).filter(
            cast(ColumnElement[bool], api_key == User.api_key)).scalar()
        try:
            my_session.execute(
                delete(Follow).returning(Follow)
                .filter(cast(ColumnElement[bool],
                             user_id == Follow.follower_id))
                .filter(cast(ColumnElement[bool],
                             following_id == Follow.following_id))
            ).one()
        except NoResultFound:
            my_session.rollback()
            return ResultModel(result=False)
        my_session.commit()
        return ResultModel(result=True)


def connect_routes_tweets_get(app: FastAPI, my_session: Session) -> None:
    """Фабрика роута получения твитов"""

    @app.get('/api/tweets',
             response_model=Union[ResultTweetsModel, ResultErrorModel])
    def get_tweets_list(
            response: Response, api_key: str = Header(...)
    ) -> Union[ResultTweetsModel, ResultErrorModel]:
        """
        Возвращает json со списком твитов
        для ленты этого пользователя из базы данных.
        В случае любой ошибки возвращает json с описанием ошибки.
        """
        try:
            user = my_session.query(User).filter(
                cast(ColumnElement[bool], api_key == User.api_key)).one()
            tweets = my_session.query(Tweet).filter(
                cast(ColumnElement[bool], user.id != Tweet.user_id)).all()
            return ResultTweetsModel(result=True, tweets=tweets)
        except (NoResultFound, MultipleResultsFound):
            response.status_code = 400
            exc_info = sys.exc_info()
            er_type = str(exc_info[0])
            er_message = ', '.join(exc_info[1].args) if exc_info[1] \
                else 'No message'
            return ResultErrorModel(
                result=False, error_type=er_type, error_message=er_message
            )


def connect_routes_users_get(app: FastAPI, my_session: Session) -> None:
    """Фабрика роутов получения пользователей"""

    @app.get('/api/users/me', response_model=ResultUserInfoModelOut)
    def get_my_info(api_key: str = Header(...)) -> ResultUserInfoModelOut:
        """
        Возвращает из базы данных запись профиля текущего пользователя.
        Возвращает json с информацией о пользователе, подписках и подписчиках.
        """
        user = my_session.query(User).filter(
            cast(ColumnElement[bool], api_key == User.api_key)).one()
        return ResultUserInfoModelOut(result=True, user=user)

    @app.get('/api/users/{user_id}', response_model=ResultUserInfoModelOut)
    def get_any_user_info(user_id: int = Path(...)) -> ResultUserInfoModelOut:
        """
        Возвращает из базы данных запись произвольного профиля по его id.
        Получает id пользователя.
        Возвращает json с информацией о пользователе, подписках и подписчиках.
        """
        user = my_session.query(User).filter(
            cast(ColumnElement[bool], user_id == User.id)).one()
        return ResultUserInfoModelOut(result=True, user=user)


def connect_routes(app: FastAPI, my_session: Session) -> None:
    """Функция-фабрика подключения роутов к приложению"""
    connect_routes_tweets_post_delete(app=app, my_session=my_session)
    connect_routes_medias_post_get(app=app, my_session=my_session)
    connect_routes_likes_post(app=app, my_session=my_session)
    connect_routes_likes_delete(app=app, my_session=my_session)
    connect_routes_follows_post(app=app, my_session=my_session)
    connect_routes_follows_delete(app=app, my_session=my_session)
    connect_routes_tweets_get(app=app, my_session=my_session)
    connect_routes_users_get(app=app, my_session=my_session)
