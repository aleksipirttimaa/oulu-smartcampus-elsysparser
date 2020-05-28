FROM python:3.7-alpine

WORKDIR /var/elsysparser

COPY elsysparser/ /usr/src/elsysparser
COPY elsysparser/requirements.txt ./

# you can mount config with:
# --volume ./server.conf:/var/elsysparser/server.conf:ro

RUN touch /var/elsysparser/main.log \
 && chmod 666 /var/elsysparser/main.log \
 && pip install --no-cache-dir -r requirements.txt

CMD ["python", "/usr/src/elsysparser/main.py"]
