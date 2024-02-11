#!/bin/bash
eval "$(cat .env | tr '\n' ' ') python main.py"
