#!/bin/sh


if [ "$FLASK_ENV" = "development" ]
then
    echo "env:development"
fi

exec "$@"
