#!/bin/bash

if docker ps -a --format '{{.Names}}' | grep -q "backend"; then
    echo "Stopping container 'backend'..."
    docker compose down backend
else
    echo "Container 'backend' is not running."
fi


export SHUFFLE_OPENSEARCH_URL="https://localhost:9200"
export SHUFFLE_ELASTIC=true
export SHUFFLE_OPENSEARCH_USERNAME=admin
export SHUFFLE_OPENSEARCH_PASSWORD=admin
export SHUFFLE_OPENSEARCH_SKIPSSL_VERIFY=true

cd backend/go-app
go run main.go walkoff.go docker.go 