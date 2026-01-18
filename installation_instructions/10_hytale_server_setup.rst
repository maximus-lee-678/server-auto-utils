Chapter 10: Hytale Server Setup
===============================
| This section assumes you have SSH access to your Oracle VM instance and are logged in as the opc user, the default user for Oracle Cloud Infrastructure.
| It also assumes you have installed Java 25.
| It also assumes you have completed the steps in Chapter 7 to set up server_auto_utils and configure env.json.
| Instructions adapted from `Hytale Server Manual <https://support.hytale.com/hc/en-us/articles/45326769420827-Hytale-Server-Manual>`_.
|
- `10.1. Uploading the Hytale Server`_
- `10.2. Uploading a Hytale World`_
- `10.3. Starting the Hytale Server`_

10.1. Uploading the Hytale Server
---------------------------------
1. Download hytale-downloader.zip from `here <https://downloader.hytale.com/hytale-downloader.zip>`_ (if you don't trust my links go to the Server Manual yourself!).
2. Extract it and run the appropriate file (Windows or Linux).
3. Follow the OAuth2 authentication instructions.
4. Upload the archive to your Oracle VM instance.
5. Extract the archive to your desired location (replace <downloaded_archive> with actual file name).

.. code-block:: console
  
  unzip -q <downloaded_archive>.zip -d .

6. Inside, there should be a "Assets.zip" and "Server" folder.

10.2. Uploading a Hytale World
------------------------------
1. If you have an existing local world you want to use, extract it from your machine. Example given is for Windows.

.. code-block:: console

  C:\Users\<user_name>\AppData\Roaming\Hytale\UserData\Saves

2. Zip it and upload it to the instance.
3. Unzip your world.

.. code-block:: console
  
  unzip -q <world_name>.zip -d .

4. The files in the "Server" folder in the 10.1 step must be copied into this created world.

.. code-block:: console

  cp -a ./Server/. ./<world_name>/

5. **(Optional)** Clean up unneeded files and rename uploaded world

.. code-block:: console
  
  rm <world_name>.zip
  rm -rf ./Server
  mv <world_name> Server

10.3. Starting the Hytale Server
--------------------------------
1. Move into the server_auto_utils file and run the following command to start the server. The command starts ALL instances defined in env.json. To specify, provide instance names as arguments.

  - If files have been renamed, change the values accordingly.

.. code-block:: console

  cd server_auto_utils/ez_start
  ./start.sh
  
2. To attach to the tmux session running the server, run the following command.

  - If the tmux session name has been changed, change the value accordingly.

.. code-block:: console

  tmux attach -t hytale

3. **(IMPORTANT)** first run step: Authentication is needed for the first run. After the server starts, you will be prompted to login. Run the following command:

.. code-block:: console

  /auth login device

4. **(IMPORTANT)** Visit the OAuth verification link displayed in the console and follow the instructions.
5. **(IMPORTANT)** Once done, you will see that "WARNING: Credentials stored in memory only - they will be lost on restart!". To store your token on the server, run:

.. code-block:: console

  /auth persistence encrypted

6. **(IMPORTANT)** Once steps 3-5 are done, the token should be good forever, as it `refreshes itself<https://support.hytale.com/hc/en-us/articles/45328341414043-Server-Provider-Authentication-Guide>`_ when it's about to expire.
7. To detach from the tmux session, press **Ctrl + B** followed by **D**.
