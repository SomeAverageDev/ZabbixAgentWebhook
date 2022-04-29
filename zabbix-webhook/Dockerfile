#########
# BUILD #
#########
FROM python:3.10-alpine as base

RUN mkdir /svc
WORKDIR /svc
COPY src/requirements.txt .

RUN rm -rf /var/cache/apk/* && \
    rm -rf /tmp/*

RUN apk update

RUN apk add --update \
    curl \
    python3 \ 
#    pkgconfig \ 
#    python3-dev \
#    openssl-dev \ 
#    libffi-dev \ 
#    musl-dev \
#    make \ 
#    gcc \
#    jpeg-dev zlib-dev \
#    libmagic \
#    libpq-dev \
    && rm -rf /var/cache/apk/* \
    && pip wheel --no-cache-dir -r requirements.txt --wheel-dir=/svc/wheels

# the wheels are now here: /svc/wheels

##########
# MASTER #
##########
FROM python:3.10-alpine

RUN apk add --no-cache
#    jpeg-dev zlib-dev \
#    libmagic

COPY --from=base /svc /svc

# create group and user used in this container
WORKDIR /svc
RUN pip install --no-cache-dir --no-index --find-links=/svc/wheels -r requirements.txt && \
    mkdir -p /app && \
    addgroup appgroup && \
    adduser -D appuser -G appgroup && \
    chown -R appuser:appgroup /app

# create and set working directory
WORKDIR /app

# copy app code into container
#COPY --chown=appuser:appgroup entrypoint.prod.sh .
COPY --chown=appuser:appgroup ./src/ ./

USER appuser

# set env variables
ENV WEBSITES_PORT 80
ENV ZWL_PORT ${WEBSITES_PORT}

ENV PYTHONPATH "${PYTHONPATH}:/app/app"
# Prevents Python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE 1
# Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED 1

EXPOSE ${ZWL_PORT}/tcp

HEALTHCHECK --interval=1m --timeout=10s --retries=3 CMD curl --fail http://localhost:${ZWL_PORT}/health || exit 1

# run entrypoint.prod.sh
ENTRYPOINT ["/bin/sh"]
#CMD ["-c", "gunicorn --bind ${ZWL_BIND:-0.0.0.0}:${WEBSITES_PORT:-${ZWL_PORT}} --timeout 600 --log-level=DEBUG --workers ${ZWL_WORKERS:-1} --threads ${ZWL_THREADS:-4} app.main:app --worker-class uvicorn.workers.UvicornH11Worker"]
CMD ["-c", "uvicorn app.main:app --host 0.0.0.0 --port $WEBSITES_PORT"]
