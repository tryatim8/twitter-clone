from typing import List

from sqlalchemy import (
    JSON,
    Column,
    ForeignKey,
    Integer,
    LargeBinary,
    PrimaryKeyConstraint,
    String,
)
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import Mapped, relationship

from backend_server.database import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    api_key = Column(String(50), nullable=False, unique=True)
    name = Column(String(50), nullable=False)
    tweets: Mapped[List['Tweet']] = relationship(back_populates='author')
    liked_tweets: Mapped[List['Tweet']] = relationship(
        secondary='like', back_populates='users_who_liked'
    )
    following: Mapped[List['Follow']] = relationship(
        foreign_keys='Follow.follower_id',
        back_populates='follower', uselist=True
    )
    followers: Mapped[List['Follow']] = relationship(
        foreign_keys='Follow.following_id',
        back_populates='following_user'
    )
    likes: Mapped[List['Like']] = relationship(
        foreign_keys='Like.user_id',
        back_populates='user_who_liked', viewonly=True
    )


class Tweet(Base):
    __tablename__ = 'tweet'

    id = Column(Integer, primary_key=True)
    content = Column(String, nullable=False)
    media_ids = Column(JSON)
    user_id = Column(Integer, ForeignKey('user.id'))
    author: Mapped['User'] = relationship(back_populates='tweets')
    medias: Mapped[List['Media']] = relationship(back_populates='tweet')
    users_who_liked: Mapped[List['User']] = relationship(
        secondary='like', back_populates='liked_tweets')
    likes: Mapped[List['Like']] = relationship(
        foreign_keys='Like.tweet_id',
        back_populates='tweet_was_liked', viewonly=True
    )


class Media(Base):
    __tablename__ = 'media'

    id = Column(Integer, primary_key=True)
    file = Column(LargeBinary, nullable=False)
    tweet_id = Column(Integer, ForeignKey('tweet.id'))
    tweet: Mapped['Tweet'] = relationship(back_populates='medias')


class Like(Base):
    __tablename__ = 'like'
    __table_args__ = (PrimaryKeyConstraint(
        'tweet_id', 'user_id', name='tweet_user_pk'), )

    tweet_id = Column(Integer, ForeignKey('tweet.id'))
    user_id = Column(Integer, ForeignKey('user.id'))
    tweet_was_liked: Mapped['Tweet'] = relationship(
        back_populates='likes', viewonly=True, foreign_keys='Like.tweet_id'
    )
    user_who_liked: Mapped['User'] = relationship(
        back_populates='likes', viewonly=True, foreign_keys='Like.user_id'
    )
    name = association_proxy('user_who_liked', 'name')


class Follow(Base):
    __tablename__ = 'follow'
    __table_args__ = (PrimaryKeyConstraint('follower_id', 'following_id',
                                           name='user_follower_pk'), )

    follower_id = Column(Integer, ForeignKey('user.id'))
    following_id = Column(Integer, ForeignKey('user.id'))
    # Для получения подписок делаем join по follower_id
    follower: Mapped['User'] = relationship(back_populates='following',
                                            foreign_keys='Follow.follower_id')
    # Для получения подписчиков делаем join по following_id
    following_user: Mapped['User'] = relationship(
        foreign_keys='Follow.following_id', back_populates='followers'
    )
    # Прокси follower_id -> id
    id = association_proxy('follower', 'id')
    name = association_proxy('follower', 'name')
