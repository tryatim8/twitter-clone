from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn


app = FastAPI()


@app.get("/index")
def read_main():
    return FileResponse("static/index.html")


app.mount("/static", StaticFiles(directory="../frontend_client/static"), name="static")
app.mount("/js", StaticFiles(directory="../frontend_client/static/js"), name="js")
app.mount("/css", StaticFiles(directory="../frontend_client/static/css"), name="css")
app.mount("/images", StaticFiles(directory="../frontend_client/static/images"), name="css")


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=5000)