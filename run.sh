#!/bin/sh

COMMAND="python3.5 bot.py"
LOGFILE=boot.txt

writelog()
{
  now=`date`
  echo "$now $*" >> $LOGFILE
}

writelog "Starting"
while true ; do
  $COMMAND
  writelog "Exited with status $?"
  writelog "Restarting"
done