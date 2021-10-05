#!/usr/bin/env bash

while true;
do
    python3 recon.py || echo "$?" && i3lock --color 000000
done

