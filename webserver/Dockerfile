FROM ubuntu:20.04

RUN apt-get update && apt-get upgrade -y

RUN apt-get install software-properties-common -y

RUN add-apt-repository ppa:deadsnakes/ppa -y

RUN apt-get update && apt-get install -y \
        python3.9 \
        python3.9-dev \
        python3-pip

# opencv-python lib deps
RUN apt-get install -y \
        libsm6 \
        libxext6 \
        libxrender-dev

# install postgres devtools
RUN apt-get update && apt-get install -y \
        libpq-dev \
        curl 

RUN pip --version

RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python3.9

COPY requirements.txt /app/

RUN python3.9 -m pip --version

RUN python3.9 -m pip install -r /app/requirements.txt

ADD . /app
WORKDIR /app

CMD ["python3.9", "server.py", "--develop"]
