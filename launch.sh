# Run this script to initialize the display and start the docker
# container and launch the GUI

if [ "$(uname)" == "Darwin" ]; then
    # For macOS
    tmpIP=$(ifconfig en0 | grep inet | awk '$1=="inet" {print $2}')
    xhost + $tmpIP
    docker-compose -f docker-compose-mac.yml run -e DISPLAY=$tmpIP:0 fuse-gui /app/code/start.sh
elif [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
    # For Linux
    xhost local:root && docker-compose run -e DISPLAY=$DISPLAY fuse-gui /app/code/start.sh
fi

docker-compose down
