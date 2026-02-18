#!/bin/sh
set -e

exec litestar --app main:app run --host 0.0.0.0 --port "${PORT:-8000}"
