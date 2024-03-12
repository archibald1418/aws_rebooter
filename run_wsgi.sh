#!/bin/bash

uvicorn --host 0.0.0.0 --port 8000 --app-dir ./api --env-file .env main:app --reload
