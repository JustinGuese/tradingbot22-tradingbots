FROM python:3.10-slim
RUN mkdir -p /app/
WORKDIR /app
RUN apt update && apt install git -y
RUN pip install -U git+https://github.com/JustinGuese/tradingbot22-basebot/
RUN apt remove git -y
RUN apt autoremove -y
RUN apt clean
COPY ./src/requirements.txt .
RUN pip install -r requirements.txt
COPY ./src/earningscalbot.py /app/
CMD ["python", "earningscalbot.py"]