#!/usr/bin/env bash

# Upload via curl
curl --form projectName=$1 --form file=@Dockerfile --trace upload.log http://127.0.0.1:8000/upload/