from typing import Optional, Iterable, List

from pydantic import BaseModel


class ResultModel(BaseModel):
    """Возвращает информацию о статусе операции"""
    result: bool


class ResultTweetModel(ResultModel):
    """Возвращает результат и tweet_id"""
    tweet_id: int


class ResultMediaModel(ResultModel):
    """Возвращает результат и media_id"""
    media_id: int


class UserModel(BaseModel):
    """Модель автора для возвращения пользователю"""
    id: int
    name: str

    class Config:
        from_attributes = True


class LikeModel(BaseModel):
    """Модель лайка для возвращения пользователю"""
    user_id: int
    name: str

    class Config:
        from_attributes = True


class TweetModel(BaseModel):
    """Модель твита для возвращения пользователю"""
    id: int
    content: str
    attachments: Optional[Iterable[int]] = None
    user: UserModel
    likes: List[LikeModel]

    class Config:
        from_attributes = True


class ResultTweetsModel(ResultModel):
    """Возвращает результат и список твитов"""
    tweets: List[TweetModel]


class ResultErrorModel(ResultModel):
    """Возвращает результат, тип исключения и сообщение исключения"""
    result: bool
    error_type: str
    error_message: str


class UserInfoModel(UserModel):
    """Модель пользователя для возвращения ему"""
    followers: List[UserModel]
    following: List[UserModel]


class ResultUserInfoModelOut(ResultModel):
    user: UserInfoModel
