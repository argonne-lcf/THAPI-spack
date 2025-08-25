#!/bin/bash

if command -v "ruff" > /dev/null 2>&1; then
  echo "Running ruff format ..."
else
  echo "Please install ruff before running $0!"
  exit 1
fi

check=0
if [ $# -gt 0 ]; then
  if [ "$1" = "--check" ]; then
    check=1
  else
    echo "Unknown command line argument: $1"
    exit 1
  fi
fi

for p in `ls packages/**/package.py`; do
  sed -i '/version(/i\    # fmt: off' $p
  sed -i '/version(/a\    # fmt: on' $p
  sed -i '/variant(/i\    # fmt: off' $p
  sed -i '/variant(/a\    # fmt: on' $p
done

ruff format

for p in `ls packages/**/package.py`; do
  sed -i '/# fmt: off/d' $p
  sed -i '/# fmt: on/d' $p
done

exit_status=0
if [ $check -eq 1 ]; then
  exit_status=`git diff | wc -l`
fi
exit $exit_status
