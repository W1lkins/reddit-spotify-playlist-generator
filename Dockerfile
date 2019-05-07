FROM python:3.7.3-slim-stretch

ADD . /app
WORKDIR /app

RUN pip install -r requirements.txt

CMD ["./generate.py"]
