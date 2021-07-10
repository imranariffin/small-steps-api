ARG BUILD_ENV

FROM python:3.8-slim-buster as build_base

# Install required C libraries for pscycopg2
RUN apt-get update \
    && apt-get -y install libpq-dev gcc

# Avoid running as root
RUN useradd -m -d /home/appuser -s /bin/bash appuser
USER appuser
WORKDIR /home/appuser
ENV HOME=/home/appuser

# Setup and run Python virtual environment
ENV VIRTUAL_ENV=$HOME/.venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY ./requirements-base.txt ./requirements-base.txt

# Build production and dev/test a little bit differently
FROM build_base as build_dev
ONBUILD COPY tests/ tests/
ONBUILD COPY requirements-dev.txt requirements-dev.txt
ONBUILD RUN cat ./requirements-base.txt ./requirements-dev.txt | sort > ./requirements.txt
FROM build_dev as build_test
FROM build_base as build_production
ONBUILD RUN echo "Skipping tests/ folder & requirements-dev.txt in production build"
ONBUILD RUN cat ./requirements-base.txt > ./requirements.txt
FROM build_${BUILD_ENV}

# Install dependencies
RUN python -m pip install --upgrade pip \
    && pip install -r ./requirements.txt

# Run application
COPY app/ app/
EXPOSE 8000
ENTRYPOINT ["/bin/bash", "./app/scripts/api.${BUILD_ENV}.sh"]
