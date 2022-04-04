#!/usr/bin/env bash

# Upload via curl
 curl --form description='uploaded via curl' --form file=@sample.pdf --trace upload.log http://127.0.0.1:8000/upload/