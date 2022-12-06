FROM python:3.10

WORKDIR /src

RUN pip install --upgrade pip

COPY openapi/requirements.txt .
RUN pip install -r requirements.txt

COPY alembic/ alembic/
COPY alembic.ini .
# COPY alembic/migrations.py .
COPY .coveragerc .
COPY openapi/ openapi/

CMD python alembic/migrations.py && python -m openapi
