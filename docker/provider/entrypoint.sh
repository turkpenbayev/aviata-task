#!/bin/bash
set -e

uvicorn app.main:app --host $SERVICE_HOST --port $SERVICE_PORT --workers=1