#!/usr/bin/env bash

set -e

docker-compose -f docker/docker-compose.yml -f docker/docker-compose.init.yml run coupon-api-init
