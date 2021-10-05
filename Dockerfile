FROM python:3.8-slim

RUN apt update && \
    apt upgrade && \
    apt install --no-install-recommends -y build-essential software-properties-common && \
    add-apt-repository -y ppa:deadsnakes/ppa && \
    apt -y install git && \
    apt -y install nginx && \
    apt -y install xvfb && \
    apt clean && rm -rf /var/lib/apt/lists/*

COPY ./server.pem ~/.ssh/
RUN eval "$(ssh-agent -s)"
RUN touch ~/.ssh/config
RUN echo "Host *" >> ~/.ssh/config
RUN echo "AddKeysToAgent yes" >> ~/.ssh/config
RUN echo "IdentityFile ~/.ssh/server.pem" >> ~/.ssh/config
RUN ssh-add -K ~/.ssh/server.pem

RUN git clone git@github.com:trendmate/server.git && cd server
RUN git checkout hosting
RUN virtualenv env
RUN . env/bin/activate
RUN pip install --no-cache-dir --user -r requirements.txt
RUN pip install --default-timeout=1000 --upgrade https://storage.googleapis.com/tensorflow/linux/gpu/tensorflow_gpu-2.6.0-cp38-cp38-manylinux2010_x86_64.whl
RUN pip install uwsgi
RUN pip install statsmodels 
RUN pip install spacy 
RUN python3 -m spacy download en_core_web_sm
WORKDIR /server
COPY ./server/nginx.conf /etc/nginx
RUN chmod +x ./start.sh
CMD ["./start.sh"]
EXPOSE 80