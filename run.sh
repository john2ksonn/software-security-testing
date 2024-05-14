#!/usr/bin/bash

set -xe

uid=1000
gid=100

subuidSize=$(( $(podman info --format "{{ range .Host.IDMappings.UIDMap }}+{{.Size }}{{end }}" ) - 1 ))
subgidSize=$(( $(podman info --format "{{ range .Host.IDMappings.GIDMap }}+{{.Size }}{{end }}" ) - 1 ))

podman build \
    -v "${PWD}/fuzzingbook":/home/jovyan/fuzzingbook \
    -v "${PWD}/.jupyter":/home/jovyan/.jupyter \
    --tag lmao/lel . 
podman run -ti --rm -p 8888:8888 \
    -v "${PWD}/fuzzingbook":/home/jovyan/fuzzingbook \
    -v "${PWD}/work":/home/jovyan/work \
    -v "${PWD}/.jupyter":/home/jovyan/.jupyter \
    --uidmap $uid:0:1 --uidmap 0:1:$uid --uidmap $(($uid+1)):$(($uid+1)):$(($subuidSize-$uid)) \
    --gidmap $gid:0:1 --gidmap 0:1:$gid --gidmap $(($gid+1)):$(($gid+1)):$(($subgidSize-$gid)) \
    --name 'fuzzingbook' \
    lmao/lel

