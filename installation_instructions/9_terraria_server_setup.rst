Chapter 9: Terraria Server Setup
=================================
| This section assumes you have SSH access to your Oracle VM instance and are logged in as the opc user, the default user for Oracle Cloud Infrastructure.
| It also assumes you have installed Mono.
| It also assumes you have completed the steps in Chapter 7 to set up server_auto_utils and configure env.json.
|
- `9.1. Uploading your Terraria World`_
- `9.2. Starting your Terraria Server`_

9.1. Uploading your Terraria World
----------------------------------
1. Download the latest Terraria `server files <https://terraria.wiki.gg/wiki/Server#Downloads>`_.
2. Pull out the "\\<version>\\Linux" directory from the downloaded archive and zip it into a new archive.
3. Upload the archive to your Oracle VM instance.
4. Extract the archive to your desired location.

  .. code-block:: console
    
    unzip -q Linux.zip -d .

5. Because we are using Mono to run the Terraria server, the following extra steps are required.

  .. code-block:: console

    cd Linux
    rm System*
    rm Mono*
    rm monoconfig
    rm mscorlib.dll
    cd ../

6. Follow standard terraria server setup procedures to configure the server, i.e. setting up and uploading serverconfig.txt (very important).

9.2. Starting your Terraria Server
----------------------------------
1. Move into the server_auto_utils file and run the following command to start the server. The command starts ALL instances defined in env.json. To specify, provide instance names as arguments.

  - If files have been renamed, change the values accordingly.

  .. code-block:: console

    cd server_auto_utils/ez_start
    ./start.sh

2. To attach to the tmux session running the server, run the following command.

  - If the tmux session name has been changed, change the value accordingly.
  
  .. code-block:: console
  
    tmux attach -t terraria

3. To detach from the tmux session, press **Ctrl + B** followed by **D**.
