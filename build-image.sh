#!/bin/sh

docker image prune --filter "until=30m" -f
docker container prune --filter "until=1h" -f
docker network prune --filter "until=24h" -f
docker builder prune --filter "until=1h" -f

docker-compose -f docker-compose.prod.yml down -v
DOCKER_BUILDKIT=1 docker-compose -f docker-compose.prod.yml build --no-rm
DOCKER_BUILDKIT=1 docker-compose -f docker-compose.prod.yml up

