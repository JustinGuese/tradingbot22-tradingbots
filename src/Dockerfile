FROM python:3.10-slim
RUN mkdir /app
WORKDIR /app
COPY requirements.txt /app
RUN pip install -r requirements.txt
COPY ./basebot.py /app/
COPY rsiexamplebot.py /app/
CMD ["python", "rsiexamplebot.py"]