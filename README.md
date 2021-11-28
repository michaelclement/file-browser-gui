# Final Project for Operating Systems (CSC 5422)
**Fall 2021**

This project is a graphical user interface for a filesystem in
userspace (or a regular filesystem).

## Disclaimer
The FUSE in use is a modified example from
[stavros.io](https://www.stavros.io/posts/python-fuse-filesystem/) -

My primary contribution is the GUI that sits atop the FUSE.

## Setup

*Linux and macOS*

- Install Docker and Docker-Compose
- Build the Docker image in the project root: `docker-compose build` *Note: the build takes a while*

*macOS*

- Install XQuartz: `brew cask install xquartz` *additional info about XQuartz [here](https://sourabhbajaj.com/blog/2017/02/07/gui-applications-docker-mac/)*

## Usage 

Run the `launch.sh` script in the root dir of the project. This starts a docker container
and then runs the script to launch the FUSE and GUI within that container.
