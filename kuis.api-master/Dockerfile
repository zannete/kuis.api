FROM python:3

ADD . /root/app
WORKDIR /root/app

RUN pip install -r requirements.txt

EXPOSE 3000

CMD gunicorn run:app --bind 0.0.0.0:3000