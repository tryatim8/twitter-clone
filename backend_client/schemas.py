from typing import Optional, Iterable, List

from pydantic import BaseModel


class UserModel(BaseModel):
    """Модель автора для возвращения пользователю"""
    id: int
    name: str

    class Config:
        from_attributes = True


class LikeModel(BaseModel):
    """Модель лайка для возвращения пользователю"""
    tweet_id: int
    user_id: int

    class Config:
        from_attributes = True


class TweetModelOut(BaseModel):
    """Модель твита для возвращения пользователю"""
    id: int
    content: str
    attachments: Optional[Iterable[int]] = None
    user: UserModel
    likes: List[LikeModel]

    class Config:
        from_attributes = True


class UserInfoModelOut(UserModel):
    """Модель пользователя для возвращения ему"""
    followings: List[UserModel]
    followers: List[UserModel]
