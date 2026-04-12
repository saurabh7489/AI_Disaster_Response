FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 7860

ENV PYTHONPATH=/app

CMD ["sh", "-c", "python inference.py > /tmp/log.txt 2>&1; cat /tmp/log.txt; python server/app.py"]