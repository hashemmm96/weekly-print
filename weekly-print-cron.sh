#!/usr/bin/env bash
set -e

# Note: assumes there is a python venv in REPO_PATH/.venv
# Must be installed in user crontab. Example cron entry for 10:00 every sunday:
# 0 10 * * 7 $HOME/weekly-print/weekly-print-cron.sh &>> $HOME/.print-log

REPO_PATH=$(realpath $(dirname ${0}))

${REPO_PATH}/.venv/bin/python ${REPO_PATH}/weekly-print.py --image ${REPO_PATH}/rainbow.png
