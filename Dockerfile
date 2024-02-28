FROM python:3.10

# это переменная окружения, которая означает, что Python не будет пытаться создавать файлы .pyc
ENV PYTHONDONTWRITEBYTECODE 1

# выходные данные python, т.е. потоки stdout и stderr, отправляются прямо на терминал
ENV PYTHONUNBUFFERED 1

# Установливаем рабочую директорию
WORKDIR /app

COPY requirements.txt /app/
# install python dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

RUN python manage.py migrate

