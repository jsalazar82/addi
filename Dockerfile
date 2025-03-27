FROM python:3.8-slim-buster

WORKDIR /app

COPY . .

RUN pip3 install -r requirements.txt

RUN pip3 install flask flask_script flask_migrate

RUN pip3 install -U Flask-SQLAlchemy

ENV APP_SETTINGS="config.DevelopmentConfig"

#RUN pip3 install pyopenssl

RUN python3 manage.py db init

RUN python3 manage.py db migrate

RUN python3 manage.py db upgrade

ENTRYPOINT ["python3"]

CMD ["app.py"]
