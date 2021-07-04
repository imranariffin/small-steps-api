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

# Build production and dev a little bit differently
FROM build_base as build_dev
ONBUILD COPY tests/ tests/
ONBUILD COPY ./requirements-dev.txt ./requiremens-dev.txt
FROM build_base as build_production
ONBUILD RUN echo "Skipping tests/ folder & requirements-dev.txt in production build"
FROM build_${BUILD_ENV}

# Install dependencies
COPY ./requirements-base.txt ./requirements-base.txt
RUN touch ./requirements-dev.txt \
    && cat ./requirements-base.txt ./requirements-dev.txt | sort > ./requirements.txt \
    && python -m pip install --upgrade pip \
    && pip install -r ./requirements.txt

# Run application
COPY app/ app/
EXPOSE 8000
ENTRYPOINT ["uvicorn", "app.api:api", "--host", "0.0.0.0", "--port", "8000"]
