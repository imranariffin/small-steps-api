FROM python:3.8-slim-buster

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

# Install dependencies
COPY app/requirements.txt ./app/requirements.txt
RUN python -m pip install --upgrade pip \
    && pip install -r ./app/requirements.txt

# Run application
COPY app/ app/
EXPOSE 8000
ENTRYPOINT ["uvicorn", "app.api:api", "--host", "0.0.0.0", "--port", "8000"]
