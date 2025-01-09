#!/bin/bash

skyblock_folder_id="_________________________________"
gdrive_path="/home/opc/gdrive"
world_path="/home/opc/skyblock_1.19/world"
backup_path="/home/opc/backups"
tmux_session_name="skyblock"

zip_new=$(date '+world_%d%m%Y_%H%M%S.zip')
zip_old="NULL"
gdriveID_old="NULL"
was_server_running="FALSE"

getDriveID() {

gdriveID_old=$($gdrive_path list --no-header --query "'$skyblock_folder_id' in parents and name contains '$1'")

# Keep only ID
gdriveID_old=${gdriveID_old%% *}
}

################################

# Check for skyblock pane
if tmux list-session -F '#S' 2> /dev/null | grep -q "^$tmux_session_name\$"
then
	was_server_running="TRUE"

	# Shutdown server
	echo "Shutting down server!"
	tmux send-keys -t $tmux_session_name "/say Shutting down for backup! Return in 5 minutes!" Enter
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

	echo "Waiting for shutdown."
	sleep 15

fi

echo "Backup in progress!"
# Only delete oldest file if 5 files exist
if (($(ls $backup_path -l | egrep -c '^-') >= 5))
then
	# Oldest file's name
	zip_old=$(ls $backup_path -t | tail -1)
        # Removing from local and drive
	rm $backup_path/$zip_old
	getDriveID "$zip_old"
	$gdrive_path delete $gdriveID_old
fi

# Zip world
echo "Zipping world, this may take a while"
pushd $world_path > /dev/null
zip -q -r $backup_path/$zip_new .
popd > /dev/null

# Upload world
$gdrive_path upload -p $skyblock_folder_id $backup_path/$zip_new

if [ $was_server_running == "TRUE" ]
then
	# Restarting world
	echo "Restarting server!"
	cd $world_path/.. && tmux new-session -d -s $tmux_session_name 'java -Xmx8G -jar fabric-server-launch.jar nogui'
fi

echo "
[SUMMARY]
[UPLOAD] $zip_new
[DELETE] $zip_old"
