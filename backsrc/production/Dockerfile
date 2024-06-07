
# syntax=docker/dockerfile:1
FROM python:3.6

WORKDIR /kamssl

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEBUG=1
COPY requirements.txt ./
RUN echo $(python -V)
# RUN apt-get install python-setuptools python-dev

# RUN apt-get install --reinstall libpq-dev -y
# RUN apt-get install libjpeg-dev zlib1g-dev -y
# RUN apt install libpython3.7-dev -y
# RUN apt-get install python-psycopg2
# python-mysqldb
RUN python -m pip install --upgrade pip
RUN python -m pip install --upgrade setuptools
RUN python -m pip install -r requirements.txt
COPY . ./
COPY DialProCertificates/ /DialProCertificates/

#CMD ["python", "manage.py", "runsslserver", "0.0.0.0:9091"]
CMD ["gunicorn", "--keyfile", "/DialProCertificates/privkey.pem", "--certfile", "/DialProCertificates/cert.pem", "finalminutes.wsgi:application", "-w", "2", "-b", "0.0.0.0:9091"]