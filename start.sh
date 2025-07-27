#!/bin/bash
source ./directory.conf
source $GLUCOSE_DIR/venv/bin/activate
exec python -u $GLUCOSE_DIR/db_update.py
