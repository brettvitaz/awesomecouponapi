FROM python:3.6

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt

COPY ./api /usr/src/app/api
COPY coupons.json /usr/src/app/
COPY scripts/wait-for-it.sh /usr/src/app/

EXPOSE 5000/tcp

ENV PYTHONPATH=/usr/src/app/

CMD [ "./wait-for-it.sh", "coupon-db:5432", "-w", "5", "-t", "10", "-s", "--", "python", "./api/app.py" ]
