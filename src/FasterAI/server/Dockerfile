FROM python:3.10

WORKDIR /app/server

COPY ./requirements.txt /app/server

RUN pip install --no-cache-dir -r /app/server/requirements.txt

COPY . /app/server

CMD ["python", "main.py"]