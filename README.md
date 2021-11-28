# Final Project for Operating Systems (CSC 5422)

## Overview

This project is a graphical user interface for a filesystem in
userspace (or just a regular filesystem). Launching this application
will mount a FUSE, and then start a GUI that allows the user to use
the file system. 

Theoretically it can run on any platform that is compatible with
Docker (though I've not tested it on Windows).

It has the most basic of functionality. Through the GUI one can:
- create directories and files
- copy items from location to location
- delete items
- set directories as favorites for easy navigation
- view file metadata (limited)
- view and edit file contents (as long as it's text)

... and generally browse the filetree.

### Disclaimer
The FUSE in use is a not-so-modified example 
[example](https://www.stavros.io/posts/python-fuse-filesystem/).

My contribution is the GUI that sits atop the FUSE (`FileBrowser.py`).

## Setup

**The Docker Way**

- Install Docker and Docker-Compose ([Ubuntu instructions](https://docs.docker.com/engine/install/ubuntu/#install-using-the-convenience-script))

*Extra step for macOS:*
- Install XQuartz: `brew cask install xquartz` *additional info about why XQuartz is being used [here](https://sourabhbajaj.com/blog/2017/02/07/gui-applications-docker-mac/)*

**The No-Docker Way (untested)**

If you wish to avoid using Docker with this project, you can try to
run things natively.

*Linux:*

- Install Python3: `apt-get install python3 -y`
- Install PIP: `apt install python3-pip`
- Install the FUSE and Tkinter packages: 
    `apt-get install fuse -y`
    `apt-get install tk -y`
    `apt-get install python3-tk -y`
    `pip install -U fusepy --user`
- `cd` into the `code` directory and launch the Python FUSE program:
    `python3 ./fuse_ex.py ../myfiles/ ../mymnt &`
- Launch the GUI: `python3 ./main.py`

## Usage 

**The Fast & Easy Way (requires Docker and Docker-Compose)**
To get the GUI up and running, simply run the `launch.sh` script in the
root of the project. This starts a docker container and then runs the 
script to launch the FUSE and GUI within that container.

**The Slightly Less Fast & Easy Way (for command-line FUSE access)**
To verify that a FUSE is indeed running underneath the GUI, you can
start things up more piecemeal. 

- Launch a shell in the docker container: `xhost local:root && docker-compose run -e DISPLAY=$DISPLAY fuse-gui bash`

- Start the FUSE and GUI by running: `./code/start.sh &` in the root of 
the running Docker container

- Inspect the newly mounted FUSE by running an `ls` on the `/app/mymnt`
directory. The files from `/app/myfiles` have been mounted and should
show up there. `/app/mymnt` is then interacted with by the GUI.

- The GUI should have started after running the `start.sh` script, so
use that window as normal.

Due to how the Docker environment is set up, any file changes made 
through the GUI will persist after things shut down. They will be
found in the `myfiles` dir.
