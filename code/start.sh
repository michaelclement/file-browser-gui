#!/bin/bash
# This script launches the FUSE and GUI.

# Make sure we're in the right location
workdir=$(pwd)
if [[ $workdir != /app/code ]];
then
    echo 'Changing pwd to /app/code...';
    cd /app/code;
fi

# Start the FUSE if it's not already running
mounted=$([ "$(ls /app/mymnt)" ] && echo "Not empty" || echo "Empty");
if [[ $mounted = "Empty" ]];
then
    # (We assume an empty mount point means FUSE
    # isn't running. That could be false, but for my
    # purposes we'll just let it slide)
    echo 'Starting FUSE...';
    python3 ./fuse_ex.py ../myfiles/ ../mymnt/ &
else
    echo 'FUSE already running...';
fi

echo 'Starting GUI...';
python3 ./main.py;

echo 'Done...';