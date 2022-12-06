FROM python:3.10-slim
RUN mkdir -p /app/
WORKDIR /app
COPY ./src/requirements.txt .
RUN pip install -r requirements.txt
COPY ./src/checkbreakout.py /app/
CMD ["python", "checkbreakout.py"]