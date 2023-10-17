#!/bin/bash

docker build -t visglm .
docker run -it \
 -p 8080:8080 \
 -v {your_model_path}:/app/model_hub/ --runtime=nvidia -e NVIDIA_VISIBLE_DEVICES=all visglm
