from sqlalchemy import Column, Integer, String, ARRAY, LargeBinary, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import relationship

from database import Base, engine, session


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    api_key = Column(String(50), nullable=False, unique=True)
    name = Column(String(50), nullable=False)


class Tweet(Base):
    __tablename__ = 'tweet'

    id = Column(Integer, primary_key=True)
    content = Column(String, nullable=False)
    attachments = Column(ARRAY(Integer))
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



class Follow(Base):
    __tablename__ = 'follow'
    __table_args__ = (PrimaryKeyConstraint('follower_id', 'following_id', name='user_follower_pk'), )

    follower_id = Column(Integer, ForeignKey('user.id'))
    following_id = Column(Integer, ForeignKey('user.id'))
    # Для получения подписок делаем join по follower_id
    follower = relationship('User', backref='followings', foreign_keys='Follow.follower_id')
    # Для получения подписчиков делаем join по following_id
    following = relationship('User', backref='followers', foreign_keys='Follow.following_id')


if __name__ == '__main__':
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    user1: User = User(api_key='test1', name='name_one')
    user2: User = User(api_key='test2', name='name_two')
    follow_1_2: Follow = Follow(follower_id=1, following_id=2)
    follow_2_1: Follow = Follow(follower_id=2, following_id=1)
    session.add_all([user1, user2, follow_1_2, follow_2_1])

    media: Media = Media(file=b'abcdef')
    tweet1: Tweet = Tweet(content='some_text', attachments=[1])
    tweet1.medias.append(media)
    user1.tweets.append(tweet1)
    user2.liked_tweets.append(tweet1)
    tweet1.users_who_liked.append(user1)

    session.commit()
