#!/bin/bash
screen -ls | grep rubyrose | cut -d. -f1 | awk "{print $1}" | xargs kill
screen -dmS rubyrose bash -c "cd /path/to/bot; python3.6 bot.py; exec bash"
