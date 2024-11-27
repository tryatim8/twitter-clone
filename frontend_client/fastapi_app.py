from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles


def create_app() -> FastAPI:
    """Инициализация объекта приложения"""
    _app = FastAPI()
    return _app


def connect_route_index(app: FastAPI) -> None:
    """Фабрика подключения роута к приложению"""
    @app.get("/index")
    def read_main() -> FileResponse:
        """Рендер статики html-файла"""
        return FileResponse("../frontend_client/static/index.html")


def mount_static(app: FastAPI) -> None:
    """Функция монтирования файлов статики к приложению"""
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
