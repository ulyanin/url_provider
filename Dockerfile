FROM python:3.7.3

EXPOSE 3030

RUN apt-get update &&\
    apt-get install -y --no-install-recommends libev4 libev-dev cython3

RUN mkdir -p /app/src
WORKDIR /app/src
COPY . .
RUN python3 setup.py install
WORKDIR /app/src/mas
CMD python3 cli.py --port 3030