FROM python:3.10-slim
RUN mkdir /app
WORKDIR /app
COPY requirements.txt /app
RUN pip install -r requirements.txt
COPY ./basebot.py /app/
COPY trendbot.py /app/
CMD ["python", "trendbot.py"]