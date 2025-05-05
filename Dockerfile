FROM python:3.13-slim

ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app/

COPY . .


RUN pip install --no-cache-dir poetry \
    && poetry config installer.max-workers 5 \
    && poetry install --no-interaction --no-ansi

RUN opentelemetry-bootstrap -a install


EXPOSE 8000
CMD [ "opentelemetry-instrument ","poetry", "run", "uvicorn", "--host", "0.0.0.0", "vender_api.app:app" ]