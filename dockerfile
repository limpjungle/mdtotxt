FROM python:3.11-slim
WORKDIR /data 
COPY convert.py /app/convert.py 
RUN pip install --no-cache-dir markdown beautifulsoup4
ENTRYPOINT ["python", "/app/convert.py"]

