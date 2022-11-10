#!/bin/bash
set -e

sleep 10

exec celery -A app beat -l info