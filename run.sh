#!/bin/bash

source ./env/bin/activate
./docker/configure.sh
uvicorn olp.app:app --reload
