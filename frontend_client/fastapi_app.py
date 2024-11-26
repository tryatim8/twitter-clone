from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles


def create_app():
    """Инициализация объекта """
    _app = FastAPI()
    return _app


def connect_route_index(app: FastAPI):
    @app.get("/index")
    def read_main():
        return FileResponse("../frontend_client/static/index.html")


def mount_static(app: FastAPI):
    app.mount("/static", StaticFiles(directory="../frontend_client/static"),
              name="static")
    app.mount("/js", StaticFiles(directory="../frontend_client/static/js"),
              name="js")
    app.mount("/css", StaticFiles(directory="../frontend_client/static/css"),
              name="css")
    app.mount("/images",
              StaticFiles(directory="../frontend_client/static/images"),
              name="css")


application = create_app()
connect_route_index(app=application)
