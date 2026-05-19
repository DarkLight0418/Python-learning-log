FROM python:3.14-slim

WORKDIR /chatapp

COPY server.py .
COPY protocol.py .

EXPOSE 5000

CMD [ "python", "server.py" ]