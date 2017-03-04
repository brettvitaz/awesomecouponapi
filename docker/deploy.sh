#!/usr/bin/env bash

set -e

export POSTGRES_USER=${1:-postgres}
export POSTGRES_PASSWORD=${2:-postgres}

docker-compose -f docker/docker-compose.yml up -d
