Chapter 6: Minecraft Server Setup
=================================
| This section assumes you have SSH access to your Oracle VM instance and are logged in as the opc user, the default user for Oracle Cloud Infrastructure.
|
- `6.1. Setting Up of server_auto_utils`_
- `6.2. Uploading your Minecraft World`_
- `6.3. Crontab Updates`_
- `6.4. Starting your Minecraft Server`_

6.1. Setting Up of server_auto_utils
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

9. Make a copy of .env.example and rename it to .env.

  .. code-block:: console

    cp .env.example .env

10. Modify this copy of .env to suit your environment.

.env Configuration
~~~~~~~~~~~~~~~~~~
| Every variable in the .env file is required for the scripts to run successfully.
| Ensure that values defined are surrounded by "double quotes".
| The following variables must be set:
|
1. GDRIVE_BACKUP_FOLDER_ID
^^^^^^^^^^^^^^^^^^^^^^^^^^
- ID of the Google Drive folder where backups will be uploaded. 
- This can be found in the URL of the folder when viewed in the browser (https://drive.google.com/drive/folders/<this_string>). 
- Example Value: **Fd2HiU6O_3YaVlJGcnJqCHDp-O7vJ3N8f** (random.org moment)

2. PATH_UTILS_LOCATION
^^^^^^^^^^^^^^^^^^^^^^
- Absolute path to the server_auto_utils directory 
- Example Value: **/home/opc/server_auto_utils**

3. SERVICE_ACCOUNT_JSON_NAME
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- Name of the service account JSON file that will be used to authenticate with Google Drive.
- File is obtained in Section 5.2, and should be placed in the server_auto_utils directory.
- Example Value: **service_account.json**

4. PATH_SERVER_FOLDER
^^^^^^^^^^^^^^^^^^^^^
- Absolute path to the Minecraft server directory.
- The directory itself should directly contain the server files, like the world data, server.properties, server.jar, etc.
- Example Value: **/home/opc/server**

5. PATH_BACKUP_FOLDER
^^^^^^^^^^^^^^^^^^^^^
- Absolute path to the backup directory.
- Example Value: **/home/opc/backups**

6. BACKUP_COUNT
^^^^^^^^^^^^^^^
- Maximum number of backups to keep locally and in Google Drive.
- Example/Recommended Value: **5**

7. BACKUP_COMPRESSION_LEVEL
^^^^^^^^^^^^^^^^^^^^^^^^^^^
- Zipped file compression level.
- Example/Recommended Value: **9**

8. TMUX_SESSION_NAME
^^^^^^^^^^^^^^^^^^^^
- Name of tmux session to run the server on.
- Can be any string, and is used with **tmux attach -t <string>** to reattach to the session when logged in as opc.
- Example Value: **skyblock**

9. STARTUP_COMMAND
^^^^^^^^^^^^^^^^^^
- Command to start the server with. 
- Assumes command is run in PATH_SERVER_FOLDER.
- Use of nogui HIGHLY recommended.
- Example Value: **java -Xmx8G -jar fabric-server-launch.jar nogui**

10. SHUTDOWN_DELAY_SECONDS
^^^^^^^^^^^^^^^^^^^^^^^^^^
- Delay in seconds before the server is shut down.
- This value is used by the crontab shutdown script. 
- For example, if the value is 900, the server will shut down 15 minutes after the "Run daily Minecraft server shutdown, backup, and reboot workflow" command in the crontab is run.
- Example Value: **900**

11. FORCE_SHUTDOWN_DELAY_SECONDS
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- Delay in seconds before the server is forcefully shut down.
- This value is used by the backup and load_backup scripts when invoked while the server is still running.
- Example Value: **3**

12. REBOOT_TEMP_FILE_IND
^^^^^^^^^^^^^^^^^^^^^^^^
- Temporary file name created to indicate a restart of the minecraft server after a reboot is required.
- There's really no need to change this.
- Example/Recommended Value: **.routine_reboot**

6.2. Uploading your Minecraft World
-----------------------------------
1. Upload the archive to your Oracle VM instance.
2. Extract the archive to your desired location.

  .. code-block:: console
    
    unzip -q server.zip -d .

3. Follow standard minecraft server setup procedures to configure the server, i.e. setting up server.properties (whitelisting recommended!), eula.txt, etc.

6.3. Crontab Updates
--------------------
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
  - This can be changed by modifying the "Run daily Minecraft server shutdown, backup, and reboot workflow" line in the crontab file.

6. Save and exit the editor.

6.4. Starting your Minecraft Server
-----------------------------------
1. Move into the server_auto_utils file and run the following command to start the server.

  - If files have been renamed, change the values accordingly.

  .. code-block:: console

    cd server_auto_utils/ez_start
    ./start.sh
  
2. To attach to the tmux session running the server, run the following command.

  - If the tmux session name has been changed, change the value accordingly.

  .. code-block:: console

    tmux attach -t server

3. To detach from the tmux session, press **Ctrl + B** followed by **D**.
