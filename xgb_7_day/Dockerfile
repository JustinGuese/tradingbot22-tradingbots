FROM python:3.10-slim
RUN mkdir -p /app/persistent/
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY ./basebot.py .
COPY ./train.py .
COPY ./run.py .
CMD ["python", "run.py"]