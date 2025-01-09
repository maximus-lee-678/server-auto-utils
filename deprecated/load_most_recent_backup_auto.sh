#!/bin/bash

world_path="/home/opc/skyblock_1.19/world"
backup_path="/home/opc/backups"
tmux_session_name="skyblock"

was_server_running="FALSE"
recent_backup="NULL"
################################

if (($(ls $backup_path -l | egrep -c '^-') == 0))
then
	echo "No backups found!"
	exit 1
fi

# Check for skyblock pane
if tmux list-session -F '#S' 2> /dev/null | grep -q "^$tmux_session_name\$"
then
        was_server_running="TRUE"

        # Shutdown server
        echo "Shutting down server!"
        tmux send-keys -t $tmux_session_name "/say Shutting down to load backup! Return in 5 minutes!" Enter
        sleep 1
        tmux send-keys -t $tmux_session_name "/say t-minus 3" Enter
        sleep 1
        tmux send-keys -t $tmux_session_name "/say 2" Enter
        sleep 1
        tmux send-keys -t $tmux_session_name "/say 1" Enter
        sleep 1
        tmux send-keys -t $tmux_session_name "/say Restarting!" Enter
        sleep 1
        tmux send-keys -t $tmux_session_name "stop" Enter
fi

echo "Waiting for shutdown."
sleep 15

# Newest backup's name
recent_backup=$(ls $backup_path -t | head -1)
echo "Loading $recent_backup."

# Remove current world, unzip backup
rm -r $world_path
unzip -q $backup_path/$recent_backup -d $world_path

if [ $was_server_running == "TRUE" ]
then
        # Restarting world
        echo "Restarting server!"
        cd $world_path/.. && tmux new-session -d -s $tmux_session_name 'java -Xmx8G -jar fabric-server-launch.jar nogui'
fi
