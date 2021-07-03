FROM python:3.8-slim-buster

# Avoid running as root
RUN useradd -m -d /home/appuser -s /bin/bash appuser
USER appuser
WORKDIR /home/appuser

# Setup and run Python virtual environment
ENV VIRTUAL_ENV=./.venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN which python && which python3 && which pip

RUN python -m pip install --upgrade pip

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Run application
EXPOSE 80
ENTRYPOINT ["uvicorn", "app.main:api", "--host", "0.0.0.0", "--port", "80"]
