FROM jaredv/rq-docker:latest

COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
RUN pip install .

CMD ["rq", "worker", "-u", "redis://redis:6379", "-v"]