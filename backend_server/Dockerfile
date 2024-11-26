FROM python:3.12-slim

RUN apt-get update && /usr/bin/apt-get install -y python3-dev && rm -rf /var/lib/apt/lists/*

COPY  requirements.txt /backend_server/

RUN pip install --upgrade pip

RUN pip install -r /backend_server/requirements.txt

COPY __init__.py database.py fastapi_api.py main.py models.py routes.py schemas.py /backend_server/
COPY img_1.png img_2.png /backend_server/

WORKDIR /backend_server

CMD ["uvicorn", "main:application", "--host", "0.0.0.0", "--port", "5000", "--reload"]
