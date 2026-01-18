Chapter 4: Oracle VM Setup
==========================
| This chapter assumes you have SSH access to your Oracle VM instance and are logged in as the opc user, the default user for Oracle Cloud Infrastructure.
|
- `4.1. Updating Packages`_
- `4.2. Set the Time`_
- `4.3. Installing Required Packages`_
- `4.4. Reboot the system`_
- `4.5. Installing Python 3.12`_
- `4.6. Setting up Java 21 (Minecraft)`_
- `4.7. Setting up Mono (Terraria)`_
- `4.8. Setting up Java 25 (Hytale)`_
- `4.9. Dubious Space Reclamation (Optional)`_

4.1. Updating Packages
----------------------
Update the package list and install the latest updates.
   
.. code-block:: console

  sudo yum update

4.2. Set the Time
-----------------
Set the system time to match your timezone. (Example given is for Singapore)

.. code-block:: console

  sudo timedatectl set-timezone Singapore

4.3. Installing Required Packages
---------------------------------
tmux is a terminal multiplexer that we will use to run server processes without keeping the SSH session open.
nano is a text editor (you don't technically need this, but how big could it be) that can be used to edit files.
unzip and zip is needed for the utility to work properly.

.. code-block:: console

  sudo yum install sudo yum install tmux nano zip unzip

Other dependencies for python to function properly:

.. code-block:: console
  
  sudo yum install -y gcc openssl-devel bzip2-devel libffi-devel wget

4.4. Reboot the system
----------------------
This is so cron uses the updated timezone.

.. code-block:: console

  sudo /sbin/shutdown -r now

4.5. Installing Python 3.12
---------------------------
| **IMPORTANT:** IF YOU USE ORACLE LINUX 10 LIKE INSTRUCTED, THIS STEP IS NOT NECESSARY. IT SHIPS WITH PYTHON3.12.12.
| IF YOU DO THE FOLLOWING, YOU MAY BREAK THE INSTALL AND RUN INTO SSL ISSUES. I REPEAT, DO NOT DO THIS IF YOU ARE USING ORACLE LINUX 10.
| IF YOU ARE USING SOME OTHER IMAGE WITH PYTHON 3.12, ALSO DO NOT PERFORM THIS STEP.
| 
| Code written for this project has been developed using Python 3.12.
| Depending on your system, you may need to install Python 3.12 manually (i.e. Oracle Linux 9).
| Check your installed version with **python3 --version**.
| If you need to install Python 3.12, follow the steps below.
|
| Adapted from `tutorial <https://medium.com/@donfiealex/boost-your-python-installing-3-12-on-centos-7-04c8cdc5dd8f>`_.

1. Download and install Python 3.12.

.. code-block:: console

  cd /tmp
  wget https://www.python.org/ftp/python/3.12.8/Python-3.12.8.tgz
  tar xzf Python-3.12.8.tgz

2. Compile and install Python 3.12.

.. code-block:: console

  cd Python-3.12.8
  ./configure --enable-optimizations
  make -j$(nproc)
  sudo make install

3. Verify the installation.

.. code-block:: console

  python3 --version

4. Clean up.

.. code-block:: console

  cd ..
  sudo rm -rf Python-3.12.8 Python-3.12.8.tgz

5. **(Optional)** Register Python3.12 as a lower priority, to avoid conflicts with the system Python version.
  - Check existing Python version's priority.

  .. code-block:: console

    alternatives --display python3

  - Register Python3.12 as an alternative. In this example, number 1 is the priority, should be lower than the system Python version's priority.

  .. code-block:: console

    sudo alternatives --install /usr/bin/python3 python3 /usr/local/bin/python3.12 1

4.6. Setting up Java 21 (Minecraft)
-----------------------------------
| Java is required to run a Minecraft Server.
| As mentioned in chapter 3, Oracle Linux 8 doesn't work with Java 25, verions 26+ require Oracle Linux 9+.
|
| Different versions of minecraft require different versions of minecraft, for example:
| 1.19.4 requires Java SE 17 or newer, whereas 1.21.4 requires Java SE 21 or newer.
| Some versions also cannot use too high of a version, for example 1.19.4 breaks with Java 21, and 1.20.1 breaks with Java 25.
| This guide will show you how to install Java 21, but you can change Java version according to your server version.
| 
| The following information is taken from the minecraft wiki @ 15012026:
- From the first version of Minecraft, pre-Classic rd-132211 to 1.5.2, Minecraft requires Java 5 (1.5.0) or newer.
- From 1.6.1 (13w16a) to 1.11.2 (1.12: 17w06a), Minecraft requires Java 6 (1.6.0) or newer.
- From 1.12 (17w13a) to 1.16.5 (1.17: 21w18a), Minecraft requires Java 8 (1.8.0) or newer.
- From 1.17 (21w19a) to 1.17.1 (1.18: 1.18 Pre-release 1), Minecraft requires Java 16 or newer.
- From 1.18 (1.18 Pre-release 2) to 1.20.4 (1.20.5: 24w13a), Minecraft requires Java 17 or newer.
- From 1.20.5 (24w14a) to 1.21.11, Minecraft requires Java 21 or newer.
- Since 26.1 (26.1 Snapshot 1), Minecraft requires Java 25 or newer.
|
1. Install Java 21.

.. code-block:: console

  sudo yum install sudo yum install java-21-openjdk-headless

2. If you want another version of the jdk, you can browse what's available with:

.. code-block:: console

  yum list available java-21\*

3. Verify the installation. If a "/usr/lib/jvm/java-21-openjdk" directory is listed, it's worked.

.. code-block:: console

  ls -d /usr/lib/jvm/*

4.7. Setting up Mono (Terraria)
-------------------------------
| Mono is required to run a Terraria Server on Linux arm64 architecture.
| At the time of writing (15012026), mono-complete isn't available in the Oracle Linux 10 (x86_64) EPEL repository,
| so we gotta do a bit more work.
| Instructions adapted from `here <https://rhel.pkgs.org/10/epel-aarch64/mono-complete-6.14.1-1.el10_2.aarch64.rpm.html>`_.
|
1. Download latest epel-release rpm from http://dl.fedoraproject.org/pub/epel/10/Everything/aarch64/.
2. In the FTP portal, navigate to "/Packages/e".
3. Look for a file starting with "epel-release".
4. Download it and upload it to the /tmp/ directory of your instance.
5. Install epel-release rpm.
 
.. code-block:: console

  sudo rpm -Uvh epel-release*rpm

6. Install mono-complete.

.. code-block:: console

  sudo yum install mono-complete

7. Verify the installation.

.. code-block:: console

  mono --version

4.8. Setting up Java 25 (Hytale)
--------------------------------
| Java 25 is required to run a Hytale server.
| Hytale recommends Adoptium Temurin JDK, but it isn't available on Oracle Linux 10...
| As per their `installation instructions <https://adoptium.net/installation/linux>`_, they have only built it for images up to `version 8<https://packages.adoptium.net/ui/native/rpm/oraclelinux/>`_...
| As mentioned in chapter 3, Oracle Linux 8 doesn't work with Java 25, DON'T TRY IT!
|
| We will stick with the openJDK release.
|
1. Install Java 25.

.. code-block:: console

  sudo yum install sudo yum install java-25-openjdk-headless

2. If you want another version of the jdk, you can browse what's available with:

.. code-block:: console

  yum list available java-25\*

3. Verify the installation. If a "/usr/lib/jvm/java-25-openjdk" directory is listed, it's worked.

.. code-block:: console

  ls -d /usr/lib/jvm/*

4.9. Dubious Space Reclamation (Optional)
-----------------------------------------
| Ever wondered why 20GiB of space is being taken up by a "/dev/mapper/ocivolume-oled"? Apparently it's part of "Oracle Linux Enhanced Diagnostics".
| It stores kernel crash dumps and diagnostic tools that provide information to OCI and Oracle Linux Support when issues arise.
| The partition apparently ensures that space is reserved for that diagnostic data, so that they can still be captured even if the root filesystem is full.
| https://community.oracle.com/customerconnect/discussion/656453/oci-what-is-the-ocivolume-oled-volume-mounted-on-var-oled-filesystem
| https://blogs.oracle.com/linux/oracle-linux-enhanced-diagnostics
| 
| It used to be 10GiB on Oracle Linux 8, so I closed one eye. But in Oracle Linux 10, it occupies 20GiB, ~45% of the boot volume!
| This section outlines steps to be taken to merge /dev/mapper/ocivolume-oled back into /dev/mapper/ocivolume-root.
| Only do this if you're comfortable with not receiving Oracle Linux Support for this instance!
| **IMPORTANT**: **If the instructions are not exactly followed, the system may not boot. EXERCISE CAUTION AND READ EACH STEP CAREFULLY.**
|
| **NOTE**: I only did this because during my setup, I installed everything and afterwards realised how little space there was. The more sensible thing to do is attach a block volume for extra storage.
| **NOTE**: According to `Oracle <https://docs.oracle.com/en-us/iaas/Content/FreeTier/freetier_topic-Always_Free_Resources.htm>`_, 200GB of storage is provided for free. This 200GB INCLUDES BOOT VOLUME SIZES (i.e. each instance consumes ~47GB). 
| **NOTE**: As long as your total storage used by both boot and block volumes don't exceed 200GB, you should be fine.
| **NOTE**: I don't have any instructions for this, maybe i'll get to it one day. ¯\_(ツ)_/¯
|
| Instructions adapted from `here <https://www.reddit.com/r/oraclecloud/comments/ywwp41/reclaiming_10gb_varoled/>`_.
|
1. Run the following command, noting the name of the device mounted as /var/oled. Examine the line that contains "/var/oled", and look to the first column. e.g. /dev/mapper/ocivolume-oled.

.. code-block:: console

  cat /etc/fstab

2. If the above command displays UUIDs in the first column, run the following command. Ensure "/" is mapped to "ocivolume-root" AND "/var/oled" is mapped to "ocivolume-oled". **IF ocivolume-oled DOES NOT EXIST, I'M NOT SURE WHAT WILL HAPPEN IF YOU PROCEED.** See example below:

.. code-block:: console

  lsblk -f

.. code-block:: console

  NAME               FSTYPE      FSVER    LABEL UUID                                   FSAVAIL FSUSE% MOUNTPOINTS
  sda
  ├─sda1             vfat        FAT16          A70E-5971                                  87M    13% /boot/efi
  ├─sda2             xfs                        8c810148-6d38-4b4c-b804-63f7553717ff      1.2G    36% /boot
  └─sda3             LVM2_member LVM2 001       rhWdWA-sdG2-Bt6k-uUOX-ekrm-SYw9-2vDP8i
    ├─ocivolume-root xfs                        fa1d637b-2d39-4875-a2c3-500fd67423a5      3.7G    85% /
    └─ocivolume-oled xfs                        c894f8a3-e036-4c2c-bb50-616fefd66fe7     19.5G     2% /var/oled

3. Verify exact space occupied by /var/oled. Note down the value of "LV Size", e.g. 20.00 GiB.

.. code-block:: console

  sudo lvdisplay /dev/mapper/ocivolume-oled

4. Unmount the /var/oled filesystem. **If it fails, see steps 4 - 6. Otherwise proceed to step 7.**

.. code-block:: console

  sudo umount /var/oled

5. If you get a message that states: "umount: /var/oled: target is busy.", run this command to see what processes are using files within /var/oled:

.. code-block:: console

  sudo lsof /var/oled

6. If it's not installed, install lsof.

.. code-block:: console

  sudo yum install lsof

7. The next part is subjective. **If a critical system component is using it, then this method may not be for you. TURN BACK NOW.** If the process using it can be removed, uninstall it. Oracle Linux 8 instances may have "oswatcher". oswatcher is used to `diagnose performance issues <https://docs.oracle.com/en/operating-systems/oracle-linux/8/monitoring/monitoring-WorkingWithOSWatcherBlackBox.html>`_, so it can be uninstalled for our purposes. Oracle Linux 10 instances may have "pcp". It manifests as many processes, but all of their names start with "/var/oled/pcp/". pcp is used similarly to `diagnose performance issues <https://docs.oracle.com/en/learn/ol-pcp/>`_, so it can also be uninstalled. After removal, go back to step 3.

.. code-block:: console

  sudo yum remove oswatcher

.. code-block:: console

  sudo yum remove pcp

8. Once successfully unmounted, do this for some reason (the instructions I followed requires this):

.. code-block:: console

  sudo mkdir /var/oled/crash

9. Delete the LVM logical volume named "ocivolume-oled". You need to press "y" to confirm.
    
.. code-block:: console

  sudo lvremove /dev/mapper/ocivolume-oled

10. Extend the root logical volume by the amount you noted down earlier. In this example, it's 20G.
    
.. code-block:: console
 
  sudo lvextend -L +20G /dev/mapper/ocivolume-root

11. Expand the XFS filesystem to fill the enlarged logical volume.

.. code-block:: console
 
  sudo xfs_growfs -d /dev/mapper/ocivolume-root

12. Check that your root filesystem has grown in size. In particular, check the "/dev/mapper/ocivolume-root" Size value.

.. code-block:: console
 
  df -h

13. Edit /etc/fstab and remove the line with /var/oled or comment it out with a hash sign. See example:

.. code-block:: console
 
  sudo nano /etc/fstab

.. code-block:: console

  # UUID=c894f8a3-e036-4c2c-bb50-616fefd66fe7 /var/oled               xfs     defaults        0 0

14. It is now safe to restart your instance. Enjoy your ill-gotten gains.
