Server Auto Utils (Minecraft Server Automation Utilities)
=========================================================
- A collection of instuctions and Python Scripts to automate the management of a Minecraft server hosted on Oracle Cloud.
- Automatically stops, backs up, and restarts the server daily. Also uploads backups to Google Drive.
- Logs are kept for all actions.

About
-----
| A few years ago, I heard of a `way <https://blogs.oracle.com/developers/post/how-to-set-up-and-run-a-really-powerful-free-minecraft-server-in-the-cloud>`_ to host a powerful Minecraft server on Oracle Cloud for free.
| It worked, so to support the server I also quickly created a bunch of Bash scripts to automate the management of the server, particularly routine backups and reboots.
|
| Unfortunately, after a month or so, the instance was forcibly shut down (read more about it `here <https://github.com/maximus-lee-678/server-auto-utils/blob/main/installation_instructions/2_oci_account.rst#22-pay-as-you-go-payg>`_).
| After that, I didn't have the time to set up the server again.
| Until about 2 and a half years later!
|
| Revisiting the scripts, I realised that they don't work anymore due to changes in how Google Drive API works.
| This in addition to how messy the scripts were prompted me to rewrite the scripts.
| Since there was going to be a full rewrite, I decided to use Python instead of Bash since there's a Google Drive API library for Python.
|
| To anyone reading this, I hope you find this useful! ♪(´▽｀)

How-to
------
- Download the latest release from the `Releases <https://github.com/maximus-lee-678/server-auto-utils/releases>`_ tab.
- Follow the instructions in the `installation_instructions <https://github.com/maximus-lee-678/server-auto-utils/tree/main/installation_instructions>`_ directory.

  - Full disclaimer, there is quite a lot to read. ☜(ﾟヮﾟ☜)

Special Thanks
--------------
- `Oracle Cloud <https://www.oracle.com/cloud/>`_ - Always Free Server
- `gdrive2 <https://github.com/prasmussen/gdrive>`_ - Original Google Drive API Binary
- `PyDrive2 <https://pypi.org/project/PyDrive2/>`_ - Google Drive API Python Library
- `PuTTY <https://www.putty.org>`_ - SSH client
- `WinSCP <https://winscp.net/eng/index.php>`_ - SFTP client
