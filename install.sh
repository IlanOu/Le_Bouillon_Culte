#!/bin/bash
source env/bin/activate
pip install -r requirements.txt
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install xdotool

sudo chmod 0700 /run/user/1000