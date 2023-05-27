FROM python:3.10

WORKDIR /src

COPY openapi/requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY alembic/ alembic/
COPY alembic.ini .
COPY .coveragerc .

# Looking for changes in openapi in last layer
COPY openapi/ openapi/

CMD python alembic/migrations.py && python -m openapi
