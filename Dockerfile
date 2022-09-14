FROM python:3.10
WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

# Expects the config file to be mounted to /config/config.yml
ENTRYPOINT ["python", "/app/src/main.py", "/config/config.yml"]
