#!/bin/bash
eval "$(cat .env | tr '\n' ' ') ./venv/bin/python api/main.py"
