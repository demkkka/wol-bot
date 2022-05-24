FROM python:3.9-alpine

RUN apk update && apk upgrade && \
    apk add --no-cache bash gcc libffi-dev libc-dev 

RUN mkdir /app
ADD . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["python", "main.py"]