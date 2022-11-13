FROM python:3.8

WORKDIR /root/app/

COPY ./api/requirements.txt .

RUN apt update && apt upgrade -y && \
    apt install -y libgl1-mesa-dev && \
    pip install --upgrade pip && \
    pip install -r requirements.txt && \
    apt install npm -y && \
    npm install n -g

EXPOSE 3000
EXPOSE 8000
