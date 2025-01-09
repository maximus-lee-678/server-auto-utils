#!/bin/bash

cd skyblock_1.19 && tmux new-session -d -s skyblock 'java -Xmx8G -jar fabric-server-launch.jar nogui'
