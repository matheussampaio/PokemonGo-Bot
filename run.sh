#!/usr/bin/env bash

# Starts PokemonGo-Bot
virtualenv .

source bin/active

pip install -r requirements.txt

python pokecli.py -cf configs/config.json
