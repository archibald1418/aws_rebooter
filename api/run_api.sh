#!/bin/bash
eval "$(grep -E '^[^#]' ../.env.dev | tr '\n' ' ') ./venv/bin/python src/main.py"
