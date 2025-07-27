#!/bin/bash
source ./directory.conf
source $GLUCOSE_DIR/venv/bin/activate
exec gunicorn app:server
