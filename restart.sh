#!/usr/bin/env bash

while true;
do
    python3 recon.py || echo "$?" && i3lock -e --color 000000
done

