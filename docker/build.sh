#!/usr/bin/env bash

set -e

docker build $@ -t coupon-api:1.0 -f ./docker/api/Dockerfile .
