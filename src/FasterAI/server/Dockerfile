FROM python:3.10

WORKDIR /app/server

COPY ./requirements.txt /app/server

RUN pip install --no-cache-dir -r /app/server/requirements.txt

COPY . /app/server

EXPOSE 5000

CMD ["python", "main.py"]

HEALTHCHECK CMD curl --fail http://localhost:5000 || exit 1 