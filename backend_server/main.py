from fastapi_api import create_app, input_test_data
from routes import connect_routes
from models import Base
from database import session, engine


application = create_app()
connect_routes(app=application, my_session=session)
input_test_data(base=Base, sqlalchemy_session=session, sqlalchemy_engine=engine)
