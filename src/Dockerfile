FROM python:3.10-slim
RUN apt update && apt install git -y
RUN pip install git+https://github.com/JustinGuese/tradingbot22-basebot
RUN mkdir /app
WORKDIR /app
COPY requirements.txt /app
RUN pip install -r requirements.txt
COPY ./basebot.py /app/
COPY trendbot.py /app/
CMD ["python", "trendbot.py"]