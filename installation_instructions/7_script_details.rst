Chapter 7: Script Details
=========================
| The following scripts are available in the server_auto_utils/scripts directory, and can be run using the named bash equivalents in the ez_start directory.
| Earlier in Chapter 5, we made use of the start.sh script to start the server. This section will describe the use cases of each script.
| The following scripts are available:
|
- `7.1. start.py`_
- `7.2. stop.py`_
- `7.3. backup.py`_
- `7.4. load_backup.py`_
- `7.5. post_startup_check.py`_
- `7.6. Logging`_

7.1. start.py
-------------
- Starts the Minecraft server in a named tmux session.

- Automatically run when:

  - post_startup_check.py detects a reboot is required.
  - backup.py and load_backup.py detected the server was running and needs to start the server again following zipping/unzipping.

- Manually run when:

  - The server is first set up.
  - The server is stopped for any reason and needs to be started again.

7.2. stop.py
------------
- The opposite of start.py, stops the Minecraft server.
- Issues a stop command to the server after a specified delay.
- This delay is set in the .env file as SHUTDOWN_DELAY_SECONDS for crontab reload workflows and FORCE_SHUTDOWN_DELAY_SECONDS for manual shutdowns.

- Automatically run when:

  - backup.py and load_backup.py detects the server is running and needs to shutdown to perform zipping/unzipping.
  - the crontab reload workflow is run.

- Manually run when:

  - The server needs to be stopped for any reason.

7.3. backup.py
--------------
- Backs up the Minecraft server directory to a zipped file in the backup directory.
- Also uploads the zipped file to a Google Drive folder, folder ID being specified in the .env file.
- Maintains a specified number of backups, deleting the oldest if the number exceeds the specified count. Count applies to local and Google Drive archives.
- If the server was running, it will stop the server before backing up. After the backup is complete, it will start the server again.
- Archive created follows the naming convention: **world_<Y%m%d_%H%M%S>.zip**

- Automatically run when:

  - The crontab reload workflow is run.

- Manually run when:

  - A backup is needed outside the crontab workflow.

7.4. load_backup.py
-------------------
- Loads a backup from the backup directory to the Minecraft server directory.
- Deletes the "world" directory in the server directory before unzipping the backup back to the "world" directory.
- If the server was running, it will stop the server before loading a backup. After the restore is complete, it will start the server again.
- A specific archive name can be specified as an argument.

  .. code-block:: console

    ./load_backup.sh world_19700101_000000.zip

- If an archive name is not specified, the script will create a user prompt.

  - If you want to load the latest backup, press **Enter** without entering a name.
  - If you want to load a specific backup, enter the name of the archive.

- Automatically run when:

  - **NEVER**

- Manually run when:

  - A backup needs to be loaded.

7.5. post_startup_check.py
--------------------------
- Checks for the existence of a temporary file created by the crontab reload workflow to indicate a server start is required.
- This is so that the server does not automatically start after a shutdown, only starting when the crontab reload workflow is run.
- Effectively does nothing if the file does not exist.

- Automatically run when:

  - The instance is rebooted (e.g. after a crontab reload workflow).

- Manually run when:

  - **NEVER**

7.6. Logging
------------
| All scripts log to the **server_auto_utils/logs** directory, in addition to stdout/stderr.
| File logs are separated by day (YYYY-mm-dd.log).
