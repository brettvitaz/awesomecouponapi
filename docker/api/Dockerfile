FROM python:3.6

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt

COPY ./api /usr/src/app/api

EXPOSE 5000/tcp

CMD [ "python", "./api/app.py" ]
