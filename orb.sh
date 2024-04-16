#!/bin/bash

if docker ps -a --format '{{.Names}}' | grep -q "orborus"; then
    echo "Stopping container 'orborus'..."
    docker compose down orborus
else
    echo "Container 'orborus' is not running."
fi

export ORG_ID=Shuffle
export ENVIRONMENT_NAME=Shuffle
export BASE_URL=https://fuzzy-potato-wr796q6q454qfv6jx-5001.app.github.dev
export DOCKER_API_VERSION=1.40

cd functions/onprem/orborus
go run orborus.go