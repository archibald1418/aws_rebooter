#!/bin/bash
eval "$(grep -E '^[^#]' ../.env.dev | tr '\n' ' ') python src/main.py"
