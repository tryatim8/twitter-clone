from typing import List, Optional

from pydantic import BaseModel, computed_field


class ResultModel(BaseModel):
    """Возвращает информацию о статусе операции"""
    result: bool


class ResultTweetModel(ResultModel):
    """Возвращает результат и tweet_id"""
    tweet_id: Optional[int]


class ResultMediaModel(ResultModel):
    """Возвращает результат и media_id"""
    media_id: Optional[int]


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
    media_ids: list[int]
    author: UserModel
    likes: List[LikeModel]

    @computed_field
    def attachments(self) -> Optional[List[str]]:
        return None if not self.media_ids else [
            f'/api/medias/{media_id}' for media_id in self.media_ids
        ]

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
