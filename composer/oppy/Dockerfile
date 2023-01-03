FROM python:3.10-slim
RUN mkdir -p /app/
WORKDIR /app
COPY ./requirements.txt .
RUN pip install -r requirements.txt
COPY ./oppy.py /app/
CMD ["python", "oppy.py"]