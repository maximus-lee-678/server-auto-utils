#!/bin/bash

echo "Shutting down server!"
tmux send-keys -t skyblock "/say Shutting down! If it is the first day of the month, the hardware is being rebooted, and the server will come online again at 4:30am." Enter
sleep 1
tmux send-keys -t skyblock "/say t-minus 3" Enter
sleep 1
tmux send-keys -t skyblock "/say 2" Enter
sleep 1
tmux send-keys -t skyblock "/say 1" Enter
sleep 1
tmux send-keys -t skyblock "/say Shut down!" Enter
sleep 1
tmux send-keys -t skyblock "stop" Enter

