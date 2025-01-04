FROM python:3.11.9
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
RUN pip3 install celery[redis] fastapi[standard]
COPY . /app
EXPOSE 8000
