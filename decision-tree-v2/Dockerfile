FROM python:3.10-slim
RUN mkdir -p /app
COPY ./requirements.txt /app/
RUN pip install -r /app/requirements.txt
COPY ./decisiontreev2.py /app/
WORKDIR /app
CMD ["python", "decisiontreev2.py"]