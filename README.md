## Twitter clone by Timofey Prokofyev
<p align="center">
  <img width="260" height="250" src="screenshots/icon.png">
</p>
<em>An Twitter-clone web server, for Python.</em>

[![Build status](https://img.shields.io/badge/build_status-passed-green)](https://docs.pytest.org/en/stable/)
[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)
[![Python Version](https://img.shields.io/badge/Python-3.12-blue)](https://gitlab.skillbox.ru/timofei_prokofev/python_advanced_diploma)
[![Nginx Version](https://img.shields.io/badge/NGINX-1.27.3-green)](https://hub.docker.com/_/nginx)
[![Fastapi Version](https://img.shields.io/badge/FastAPI-0.115.5-teal)](https://fastapi.tiangolo.com/)
[![Uvicorn Version](https://img.shields.io/badge/Uvicorn-0.32.0-purple)](https://www.uvicorn.org/)
---
Клон твиттера является отлично альтернативой некогда существовавшей популярной соцсети Twitter.
<br>Плюсы и особенности:
1. Систему легко развернуть через compose
2. Все ответы сервиса задокументированы
3. Две документации API: Swagger и Redoc
4. Система не теряет данные пользователя между запусками
5. Документация доступна в момент запуска приложения.
6. Система реализует статический и динамический контент
## Quickstart

Установите и запустите с помощью `docker compose`:

```shell
$ docker compose up --build
```
Теперь вы можете пользоваться социальной сетью: <br>
[Homepage](http://0.0.0.0:8080/)

После запуска сервера вы имеете доступ к документации API:
[Swagger docs](http://0.0.0.0:5000/docs) <br> 
[Redoc docs](http://0.0.0.0:5000/redoc)

Теперь ваши сотрудники могут пользоваться соцсетью, пока запущен сервер.
___
## Описание
* Мотивация
  * Создание веб-приложений это основа питониста, которую необходимо освоить.
  * Данная программа в процессе обучения на платформе Skillbox является финальной работой
  * Возможность применить и закрепить знания и навыки, полученные на курсе Python Advanced
  * Практический багаж для портфолио программиста, который никогда не бывает лишним.
* Цели и задачи
  * Применение вёрстки для отображения интерфейса сервиса микроблогов
  * Реляционная база данных для хранения данных пользователей и твитов (SQLAlchemyORM + PostgreSQL)
  * Реализация механизмов авторизации; получения, создания и удаления твитов лайков и подписок
  * Блочное тестирование api и app с помощью pytest
  * Статическая типизация кода с помощью линтеров isort, mypy, flake8 и соответствующих плагинов
* Достоинства
  * Многопользовательский интерфейс
  * Структурированность слоёв
  * Простота основного кода
  * Преимущественно функциональное и объектно-ориентированное программирование
## Помощь проекту
Отзывы и предложения пишите на почту tryatim8@mail.ru

Счёт для пожертвований: "1234 5678 8765 4321"
### Участники

Куратор работы
: Роман Андреев

Студент курса
: Тимофей Прокофьев
