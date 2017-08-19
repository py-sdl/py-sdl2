#!/bin/sh
set -e

if [[ "$PYVER" == "3" ]]; then
    pip3 install virtualenv
    python3 -m virtualenv pysdl2-venv
else
    pip2 install virtualenv
    python -m virtualenv pysdl2-venv
fi
