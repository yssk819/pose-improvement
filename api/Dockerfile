FROM python:3.8

WORKDIR /root/app/

COPY requirements.txt .

RUN apt update && apt upgrade -y && \
    apt install -y libgl1-mesa-dev && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

EXPOSE 8000
