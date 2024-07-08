#!/usr/bin/env bash

# TODO (GlennTatum) Add check for protoc binary before compilation
# For installation check here: https://grpc.io/docs/protoc-installation/
protoc -I . --pyi_out=. gtfs-realtime.proto