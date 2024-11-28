## Twitter clone by Timofey Prokofyev
<p align="center">
  <img width="250" height="250" src="screenshots/icon.png">
</p>
<em>Клон твиттера веб-сервер для Питона.</em><br>
<em>An Twitter-clone web server, for Python.</em>

[![Build status](https://img.shields.io/badge/build_status-passed-green)](https://docs.pytest.org/en/stable/)
[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)
[![Python Version](https://img.shields.io/badge/Python-3.12-blue)](https://gitlab.skillbox.ru/timofei_prokofev/python_advanced_diploma)
[![Nginx Version](https://img.shields.io/badge/NGINX-1.27.3-green)](https://hub.docker.com/_/nginx)
[![Fastapi Version](https://img.shields.io/badge/FastAPI-0.115.5-teal)](https://fastapi.tiangolo.com/)
[![Uvicorn Version](https://img.shields.io/badge/Uvicorn-0.32.0-purple)](https://www.uvicorn.org/)
---
Клон твиттера является отличной альтернативой некогда существовавшей популярной соцсети Twitter.
<br>Плюсы и особенности:
1. Систему легко развернуть через compose
2. Все ответы сервиса задокументированы
3. Две документации API: Swagger и Redoc
4. Система не теряет данные пользователя между запусками
5. Документация доступна в момент запуска приложения.
6. Система реализует статический и динамический контент<br>

The Twitter clone is a great alternative to the once popular social network Twitter. <br>Qualities and features:
1. The system is easy to deploy via compose
2. All service responses are documented
3. Two API documentations: Swagger and Redoc
4. The system does not lose user data between launches
5. Documentation is available at the time of application launch.
6. The system implements static and dynamic content
## Быстрый старт

Установите и запустите с помощью `docker compose`:

```shell
$ docker compose up --build
```
Теперь вы можете пользоваться социальной сетью: <br>
[Homepage](http://0.0.0.0:8080/)

После запуска сервера вы имеете доступ к документации API: <br>
[Swagger docs](http://0.0.0.0:5000/docs) <br> 
[Redoc docs](http://0.0.0.0:5000/redoc)

Теперь ваши сотрудники могут пользоваться соцсетью, пока запущен сервер.
## Quickstart

Install and run with `docker compose`:

```shell
$ docker compose up --build
```
Now you can use the social network: <br>
[Homepage](http://0.0.0.0:8080/)

After starting the server, you have access to the API documentation: <br>
[Swagger docs](http://0.0.0.0:5000/docs) <br> 
[Redoc docs](http://0.0.0.0:5000/redoc)

Now your employees can use the social network while the server is running.
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
## Description
* Motivation
  * Creating web applications is a Pythonista's basic skill that needs to be mastered.
  * This program is the final work in the process of training on the Skillbox platform
  * The opportunity to apply and consolidate the knowledge and skills acquired in the Python Advanced course
  * Practical baggage for the programmer's portfolio, which is never superfluous.
* Goals and objectives
  * Application of layout to display the service interface microblogs
  * Relational database for storing user data and tweets (SQLAlchemyORM + PostgreSQL)
  * Implementation of authorization mechanisms; getting, creating and deleting tweets, likes and subscriptions
  * API and app unit testing with pytest
  * Static code typing with isort, mypy, flake8 linters and corresponding plugins
* Qualities
  * Multi-user interface
  * Layer structure
  * Simplicity of the main code
  * Mainly functional and object-oriented -oriented programming
___
## Помощь проекту
Отзывы и предложения пишите на почту tryatim8@mail.ru

Счёт для пожертвований: "1234 5678 8765 4321"
### Участники

Куратор работы
: Роман Андреев

Студент курса
: Тимофей Прокофьев

___
## Help the project
Feedback and suggestions write to tryatim8@mail.ru

Donation account: "1234 5678 8765 4321"
### Participants

Curator of the work
: Roman Andreyev

Student of the course
: Timofey Prokofyev
