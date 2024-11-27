from fastapi import FastAPI

from backend_server.database import Base, engine, session
from backend_server.fastapi_api import create_app, input_test_data
from backend_server.routes import connect_routes

application: FastAPI = create_app()
connect_routes(app=application, my_session=session)
input_test_data(base=Base,
                sqlalchemy_session=session,
                sqlalchemy_engine=engine)
