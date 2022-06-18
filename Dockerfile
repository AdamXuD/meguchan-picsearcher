FROM python:3.9.5

ADD . /code

WORKDIR /code

RUN python3 -m pip config set global.index-url https://mirrors.cloud.tencent.com/pypi/simple

RUN pip install -r requirements.txt

CMD ["python", "./main.py"]