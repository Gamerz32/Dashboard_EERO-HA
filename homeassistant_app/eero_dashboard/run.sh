#!/bin/sh
set -eu

mkdir -p /data
chown appuser:appgroup /data

exec python3 /addon/launcher.py
