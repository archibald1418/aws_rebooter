#!/bin/bash
eval "$(grep -E '^[^#]' .env | tr '\n' ' ') ./venv/bin/python api/main.py"
