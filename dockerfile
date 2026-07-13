FROM python:3.11-slim

WORKDIR /app

COPY convert.py /app/
COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python", "convert.py"]

