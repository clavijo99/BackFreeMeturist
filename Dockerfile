FROM python:3.8.1
ENV PYTHONUNBUFFERED=1


# For localizations
RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
    build-essential \
    gdal-bin \
    python-gdal \
    python3-gdal \
    libpq-dev \
    libmariadbclient-dev \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libwebp-dev \
    gettext \
    python-psycopg2 \
 && rm -rf /var/lib/apt/lists/*

# Setup workdir
RUN mkdir /src
WORKDIR /src

# Python dependencies
COPY requirements.txt /src/
RUN pip install -r /src/requirements.txt

COPY . /src
