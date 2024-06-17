FROM python:3.10-slim


WORKDIR /app
ADD . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

#CMD ["bash", "run_server.sh"]