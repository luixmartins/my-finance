FROM python:latest 

WORKDIR /app 

COPY requirements.txt . 

RUN pip install --no-cache-dir --upgrade -r requirements.txt 

COPY . /app

EXPOSE 8000

ENTRYPOINT ["python", "manage.py", "runserver", "0.0.0.0:8000"]