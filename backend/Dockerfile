FROM python:latest AS production
RUN mkdir /app/
COPY requirements.txt /app
RUN pip install -r /app/requirements.txt
COPY . /app/

FROM production AS development
COPY devRequirements.txt /app
RUN pip install -r /app/devRequirements.txt
