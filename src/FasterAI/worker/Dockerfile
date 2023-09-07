FROM python:3.10

WORKDIR /app/worker

COPY ./requirements.txt /app/worker

RUN pip install --no-cache-dir -r /app/worker/requirements.txt

COPY . /app/server

CMD ["python", "worker.py"]