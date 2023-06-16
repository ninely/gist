#!/usr/bin/env sh

# This script is used to test the langchain.
curl "http://127.0.0.1:8000/stream" -X POST -d '{"message": "hello!"}' -H 'Content-Type: application/json'

curl "http://127.0.0.1:8000/stream/agent" -X POST -H 'Content-Type: application/json'