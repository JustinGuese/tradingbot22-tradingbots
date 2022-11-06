FROM python:3.10-slim
RUN mkdir -p /app/bestSettings/
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt
COPY ./basebot.py /app/basebot.py
COPY ./train.py /app/train.py
COPY ./act.py /app/act.py
COPY ./run.sh /app/run.sh
WORKDIR /app
RUN chmod +x run.sh
CMD ["./run.sh"]