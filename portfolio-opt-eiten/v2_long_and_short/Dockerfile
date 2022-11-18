FROM python:3.10-slim
RUN mkdir -p /app/persistent
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY ./eiten/ /app/eiten/
COPY ./basebot.py /app
COPY ./run.py /app
COPY ./rebalance.sh /app
RUN chmod +x /app/rebalance.sh
CMD ["./rebalance.sh"]