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
The FUSE in use is a not-so-modified example from
[stavros.io](https://www.stavros.io/posts/python-fuse-filesystem/).

My contribution is the GUI that sits atop the FUSE (`FileBrowser.py`).

## Setup

- Install Docker and Docker-Compose ([Ubuntu instructions](https://docs.docker.com/engine/install/ubuntu/#install-using-the-convenience-script))

*Extra step for macOS:*
- Install XQuartz: `brew cask install xquartz` *additional info about why XQuartz is being used [here](https://sourabhbajaj.com/blog/2017/02/07/gui-applications-docker-mac/)*

## Usage 

Run the `launch.sh` script in the root dir of the project. This starts a
docker container and then runs the script to launch the FUSE and GUI
within that container.
