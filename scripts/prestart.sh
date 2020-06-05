#! /usr/bin/env bash

echo "Waiting for Database startup..."
sleep 5

python -m application.commands conf-db
