FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

#Install packages
RUN apt-get update
RUN apt-get install -y  python3-pip
RUN pip3 install websocket-client
RUN apt-get install sshpass
COPY ./ /app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "1122"]
