FROM python:latest 

WORKDIR /app 

COPY requirements.txt . 

RUN pip install --no-cache-dir --upgrade -r requirements.txt 

# Instalar dockerize
RUN apt-get update && \
    apt-get install -y wget && \
    wget https://github.com/jwilder/dockerize/releases/download/v0.6.1/dockerize-linux-amd64-v0.6.1.tar.gz && \
    tar -C /usr/local/bin -xzvf dockerize-linux-amd64-v0.6.1.tar.gz && \
    rm dockerize-linux-amd64-v0.6.1.tar.gz

COPY . /app

EXPOSE 8000

#CMD ["sh", "-c", "dockerize -wait tcp://db:3306 -timeout 30s && python manage.py migrate && gunicorn api.wsgi:application --bind 0.0.0.0:8000"]
