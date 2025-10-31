Chapter 8: Minecraft Server Setup
=================================
| This section assumes you have SSH access to your Oracle VM instance and are logged in as the opc user, the default user for Oracle Cloud Infrastructure.
| It also assumes you have installed Java.
| It also assumes you have completed the steps in Chapter 7 to set up server_auto_utils and configure env.json.
|
- `8.1. Uploading your Minecraft World`_
- `8.2. Starting your Minecraft Server`_

8.1. Uploading your Minecraft World
-----------------------------------
1. Upload the archive to your Oracle VM instance.
2. Extract the archive to your desired location.

  .. code-block:: console
    
    unzip -q server.zip -d .

3. Follow standard minecraft server setup procedures to configure the server, i.e. setting up server.properties (whitelisting recommended!), eula.txt, etc.

8.2. Starting your Minecraft Server
-----------------------------------
1. Move into the server_auto_utils file and run the following command to start the server. The command starts ALL instances defined in env.json. To specify, provide instance names as arguments.

  - If files have been renamed, change the values accordingly.

  .. code-block:: console

    cd server_auto_utils/ez_start
    ./start.sh
  
2. To attach to the tmux session running the server, run the following command.

  - If the tmux session name has been changed, change the value accordingly.

  .. code-block:: console

    tmux attach -t server

3. To detach from the tmux session, press **Ctrl + B** followed by **D**.
