FROM python:3.10

WORKDIR /src

# Upgrade pip
RUN pip install --no-cache-dir --upgrade pip

# Install the most problematic/big libraries separately
RUN pip install --no-cache-dir llvmlite==0.39.* numba==0.56.* numpy==1.23.*

COPY openapi/requirements.txt .
# Install the rest of the requirements
RUN pip install --no-cache-dir -r requirements.txt

# Copy necessary files
COPY alembic/ alembic/
COPY alembic.ini .
COPY .coveragerc .

# Looking for changes in openapi in last layer
COPY openapi/ openapi/

CMD python alembic/migrations.py && python -m openapi
