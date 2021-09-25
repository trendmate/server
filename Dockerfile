FROM python:3.8-slim as builder
RUN apt update && \
    apt install --no-install-recommends -y build-essential gcc

RUN git clone git@github.com:trendmate/server.git
COPY ./server /server
WORKDIR /server
RUN git checkout hosting

RUN apt update && \
    apt-get -y install nginx && \
    apt install --no-install-recommends -y build-essential software-properties-common && \
    add-apt-repository -y ppa:deadsnakes/ppa && \
    apt install --no-install-recommends -y python3.8 python3-distutils && \
    update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.6 1 && \
    update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 2 && \
    apt clean && rm -rf /var/lib/apt/lists/*

RUN apt-get install xvfb
RUN pip install --no-cache-dir --user -r /requirements.txt
RUN pip install --upgrade tensorflow
COPY nginx.conf /etc/nginx
RUN chmod +x ./start.sh
CMD ["./start.sh"]
EXPOSE 80