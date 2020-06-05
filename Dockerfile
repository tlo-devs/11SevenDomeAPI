FROM tiangolo/uvicorn-gunicorn-fastapi:latest

# Install Poetry
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py \
    | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

WORKDIR /app/
COPY ["pyproject.toml", "poetry.lock", "/app/"]
RUN poetry install --no-root --no-dev

COPY ./scripts/prestart.sh ./
RUN export PYTHONPATH=${PYTHONPATH}:/app/

COPY . ./
