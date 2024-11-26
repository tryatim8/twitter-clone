from sqlalchemy import Column, Integer, String, JSON, LargeBinary, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy

from database import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    api_key = Column(String(50), nullable=False, unique=True)
    name = Column(String(50), nullable=False)


class Tweet(Base):
    __tablename__ = 'tweet'

    id = Column(Integer, primary_key=True)
    content = Column(String, nullable=False)
    media_ids = Column(JSON)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User', backref='tweets')
    users_who_liked = relationship('User', secondary='like', backref='liked_tweets')


class Media(Base):
    __tablename__ = 'media'

    id = Column(Integer, primary_key=True)
    file = Column(LargeBinary, nullable=False)
    tweet_id = Column(Integer, ForeignKey('tweet.id'))
    tweet = relationship('Tweet', backref='medias')


class Like(Base):
    __tablename__ = 'like'
    __table_args__ = (PrimaryKeyConstraint('tweet_id', 'user_id', name='tweet_user_pk'), )

    tweet_id = Column(Integer, ForeignKey('tweet.id'))
    user_id = Column(Integer, ForeignKey('user.id'))
    tweet_was_liked = relationship('Tweet', foreign_keys='Like.tweet_id', backref='likes', viewonly=True)
    user_who_liked = relationship('User', foreign_keys='Like.user_id', backref='likes', viewonly=True)
    name = association_proxy('user_who_liked', 'name')


class Follow(Base):
    __tablename__ = 'follow'
    __table_args__ = (PrimaryKeyConstraint('follower_id', 'following_id', name='user_follower_pk'), )

    follower_id = Column(Integer, ForeignKey('user.id'))
    following_id = Column(Integer, ForeignKey('user.id'))
    # Для получения подписок делаем join по follower_id
    follower = relationship('User', backref='following', foreign_keys='Follow.follower_id')
    # Для получения подписчиков делаем join по following_id
    following_user = relationship('User', backref='followers', foreign_keys='Follow.following_id')
    # Прокси follower_id -> id
    id = association_proxy('follower', 'id')
    name = association_proxy('follower', 'name')
