#!/bin/bash
set -e
source /app/venv/bin/activate
gunicorn -w 4 -b 0.0.0.0:5000 backend.app:app &
wait
