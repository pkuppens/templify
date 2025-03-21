FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml poetry.lock /app/

RUN pip install poetry && poetry install --no-dev

COPY . /app

CMD ["poetry", "run", "python"]

# This Docker container is intended for development and testing purposes.
# It allows you to run the Templify application in an isolated environment.
