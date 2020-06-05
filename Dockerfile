FROM python:3.7-alpine

WORKDIR /var/elsysparser

COPY src/ /usr/src/elsysparser
COPY certificates/ /var/elsysparser/certificates
COPY requirements.txt /var/elsysparser

# you can mount config with:
# --volume server.conf:/var/elsysparser/server.conf:ro

RUN touch /var/elsysparser/main.log \
 && chmod 666 /var/elsysparser/main.log \
 && pip install --no-cache-dir -r requirements.txt

# you can mount log with:
# --volume main.log:/var/elsysparser/main.log

CMD ["python", "/usr/src/elsysparser/main.py"]
