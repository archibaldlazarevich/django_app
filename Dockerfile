FROM python:3.12.3

ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN pip install --upgrade pip "poetry==2.1.2"

RUN poetry config virtualenvs.create false --local
COPY pyproject.toml poetry.lock ./
RUN poetry install

COPY mysite .

CMD [ 'python', 'mysite/manage.py', 'collectstatic', '|' ,'gunicorn', 'mysite.wsgi:application', '--bind', '0.0.0.0:8000']
