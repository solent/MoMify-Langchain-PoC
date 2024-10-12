# This Containerfile has been optimized following this article :
# https://medium.com/@albertazzir/blazing-fast-python-docker-builds-with-poetry-a78a66f5aed0

FROM python:3.11-buster

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

RUN apt-get update && apt-get install -y ffmpeg

RUN pip install poetry==1.8.0

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root --only main && rm -rf $POETRY_CACHE_DIR

COPY MoMify ./MoMify

RUN poetry install --only main

# Streamlit port expose
EXPOSE 8501
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["poetry", "run", "streamlit", "run", "./MoMify/app.py", "--server.port=8501", "--server.address=0.0.0.0"]