FROM python:3.12

WORKDIR /app

RUN pip install poetry

COPY poetry.lock pyproject.toml /app/

RUN poetry export -f requirements.txt --output requirements.txt

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

RUN python manage.py migrate

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
