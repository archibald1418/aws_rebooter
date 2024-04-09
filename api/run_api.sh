#!/bin/bash
eval "$(grep -E '^[^#]' .env.dev | tr '\n' ' ') ./venv/bin/python api/main.py"
