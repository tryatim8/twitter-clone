from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


engine = create_engine('postgresql+psycopg2://admin:admin@db_postgres:5432/postgres')
Session = sessionmaker(engine)
session = Session()
Base = declarative_base()
