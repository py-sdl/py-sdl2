#!/bin/sh
set -e

if [[ "$PYVER" == "3" ]]; then
    pip3 install virtualenv
    python3 -m virtualenv pysdl2-venv
else
    pip2 install virtualenv
    python2 -m virtualenv pysdl2-venv
fi

ls -al pysdl2-venv/bin
source pysdl2-venv/bin/activate
which python
which pip
