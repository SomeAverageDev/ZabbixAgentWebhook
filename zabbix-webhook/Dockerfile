#########
# BUILD #
#########
FROM python:3.9-alpine as base

RUN mkdir /svc
WORKDIR /svc
COPY src/requirements.txt .

RUN rm -rf /var/cache/apk/* && \
    rm -rf /tmp/*

RUN apk update

RUN apk add --update \
    curl \
    python3 \ 
    pkgconfig \ 
    python3-dev \
    openssl-dev \ 
    libffi-dev \ 
    musl-dev \
    make \ 
    gcc \
    jpeg-dev zlib-dev \
    libmagic \
    libpq-dev \
    && rm -rf /var/cache/apk/* \
    && pip wheel -r requirements.txt --wheel-dir=/svc/wheels

# the wheels are now here: /svc/wheels

##########
# MASTER #
##########
FROM python:3.9-alpine

RUN apk add --no-cache \
    jpeg-dev zlib-dev \
    libmagic

COPY --from=base /svc /svc

# create group and user used in this container
WORKDIR /svc
RUN pip install --no-index --find-links=/svc/wheels -r requirements.txt && \
    mkdir -p /app && \
    addgroup flaskgroup && \
    adduser -D flaskuser -G flaskgroup && \
    chown -R flaskuser:flaskgroup /app

# create and set working directory
WORKDIR /app

# copy app code into container
COPY --chown=flaskuser:flaskgroup . .
COPY --chown=flaskuser:flaskgroup ./src/ .

USER flaskuser

EXPOSE 80/tcp

HEALTHCHECK --interval=1m --timeout=10s --retries=3 CMD curl --fail http://localhost:80/health || exit 1

# run entrypoint.prod.sh
ENTRYPOINT ["./entrypoint.prod.sh"]
#CMD ["gunicorn", "-w 1", "-b 0.0.0.0:80", "--pythonpath", "/app", "app.wsgi:app"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
