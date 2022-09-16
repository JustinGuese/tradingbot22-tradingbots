FROM python:3.10-slim
RUN apt update && apt install libgomp1 -y
RUN mkdir /app
WORKDIR /app
COPY ./src/requirements.txt /app
RUN pip install -r requirements.txt
COPY ./src/basebot.py /app/
COPY ./src/lightgdm-bot.py /app/
CMD ["python", "lightgdm-bot.py"]