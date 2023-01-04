FROM python:3.10-slim
RUN mkdir -p /app/
WORKDIR /app
COPY ./requirements.txt .
RUN pip install -r requirements.txt
COPY ./smabest.csv /app/
COPY ./smaweights-tslareduced.csv /app/
COPY ./smaweights.csv /app/
COPY ./simplesma.py /app/
CMD ["python", "simplesma.py"]