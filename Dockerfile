FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT ["tail", "-f", "/dev/null"]

#CMD ["uvicorn", "sfmgraph.api:app", "--host", "0.0.0.0", "--port", "8000"] # Not ready for primetime yet. 
