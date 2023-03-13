FROM python:latest
RUN mkdir /app/
RUN pip install cassandra-driver
RUN pip install tornado
COPY . /app/
ENTRYPOINT ["python3", "/app/server.py"]
