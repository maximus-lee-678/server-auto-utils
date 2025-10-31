server_auto_utils + env.json Setup
=========================================
| This section assumes you have SSH access to your Oracle VM instance and are logged in as the opc user, the default user for Oracle Cloud Infrastructure.
|
- `7.1. Setting Up of server_auto_utils`_
- `7.2. Configuring env.json`_
- `7.3. Initialising crontab`_

7.1. Setting Up of server_auto_utils
------------------------------------
1. Get the latest release of server_auto_utils from the Releases tab.
2. Upload the archive to your Oracle VM instance.
3. Extract the archive to your desired location.

  .. code-block:: console
    
    unzip -q server_auto_utils.zip -d .

4. Alternatively, you could unzip it locally and use scp to transfer the files, either using a SCP tool like WinSCP or the command line.
5. Cd into the server_auto_utils directory.

  .. code-block:: console

    cd server_auto_utils

6. Run the following command to perform the initial setup.

  .. code-block:: console

    chmod +x setup_deps.sh && ./setup_deps.sh

7. The previous step will create a virtual environment and quick launch bash scripts which can be used to run the server_auto_utils scripts.
  | setup_deps.sh can be modified to change the following:
  - VENV_NAME: the name of the virtual environment
  - DIR_NAME_EZ_START: the name of the quick launch bash script directory

8. Move in the file "client_secrets.json" obtained in Section 5.2 to the server_auto_utils directory.

9. Make a copy of env.json.example and rename it to env.json.

  .. code-block:: console

    cp env.json.example env.json

10. Modify this copy of env.json to suit your environment (see Section 7.2).

7.2. Configuring env.json
-------------------------
| The env.json file contains configuration settings for server_auto_utils.
| Each setting is described below. Ensure that the JSON syntax is maintained when editing the file,
|
- "path_utils_location": Where the server_auto_utils directory is located.
- "service_account_json_name": Name of the service account json file for Google Drive API access.
- "routine_shutdown_delay_seconds": Delay in seconds before a routine shutdown is executed (crontab or stop.py initiated).
- "force_shutdown_delay_seconds": Delay in seconds before a forced shutdown is executed (backup.py or load_backup.py initiated).
- "reboot_temp_file": Temporary file name (created during crontab initiated reboot).
- "instances": Key-value pairs of server instances to manage, each with its own configuration. Key names are arbitrary but should be unique and identify the type of server.

  - "tmux_session_name": Name of the tmux session used to start the server process.
  - "path_server_folder": Path to the server directory.
  - "startup_command": Command to start the server. Is run from within the server directory. Do not modify this unless you know what you are doing.
  - "shutdown_commands": Commands to run when shutting down the server. Do not modify these unless you know what you are doing.

    - "timed_warn": Command to warn players of impending shutdown (soon).
    - "timed_imminent": Command to warn players of imminent shutdown (RIGHT NOW).
    - "execute": Command to actually stop the server.

  - "backup": Settings related to server backups.

    - "do": Whether to perform backups for this server instance.
    - "path_folder_to_backup": Path to the folder to be backed up (e.g. Minecraft's world folder).
    - "SECRET_target_backup_folder_gdrive_id": Google Drive folder ID for storing backups. Service account must have write access to this folder.
    - "target_backup_folder_local_path": Path to the local directory where backups are stored.
    - "arc_name_template": Template for naming backup archives. Should contain the "{timestamp}" substring.
    - "backup_count": Number of backups to retain, both in Google Drive and locally.
    - "backup_compression_level": Compression level for zip archives (0-9).

7.3. Initialising crontab
-------------------------
| crontab is a time-based job scheduler in Unix-like operating systems. It is used to schedule jobs (commands or scripts) to run periodically at fixed times, dates, or intervals.
|
1. Run the following command to open the root crontab for editing. Root is needed to issue reboot commands.

  .. code-block:: console

    sudo crontab -e

2. If you have a skill issue like me, you can use the following command to open the crontab in a more user-friendly editor.

  .. code-block:: console

    sudo EDITOR=nano crontab -e

3. Paste the values defined in the "crontab" file into the editor.
4. If the virtual environment name or utility folder name has been renamed, change the values there accordingly.
5. By default, the server is set to begin the reboot operation at 3:45 AM local time every day. 
  - This can be changed by modifying the "Run daily server shutdown, backup, and reboot workflow" line in the example crontab file.
