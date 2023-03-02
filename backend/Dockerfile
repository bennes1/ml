FROM python:latest
RUN mkdir /app/
COPY . /app/
RUN pip install cassandra-driver
ENTRYPOINT ["python3", "/app/server.py"]
