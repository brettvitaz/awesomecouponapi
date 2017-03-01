#!/usr/bin/env bash

docker build $@ -t coupon-api:1.0 -f ./docker/api/Dockerfile .
