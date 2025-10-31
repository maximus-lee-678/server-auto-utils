Section 4: Oracle VM Setup
===========================
| This section assumes you have SSH access to your Oracle VM instance and are logged in as the opc user, the default user for Oracle Cloud Infrastructure.
|
- `4.1. Updating packages`_
- `4.2. Installing tmux`_
- `4.3. Installing Python 3.12`_
- `4.4. Setting up Java (Minecraft)`_
- `4.5. Setting up Mono (Terraria)`_

4.1. Updating packages
----------------------
Update the package list and install the latest updates.
   
  .. code-block:: console

    sudo yum update

4.2. Installing tmux
--------------------
tmux is a terminal multiplexer that we will use to run server processes without keeping the SSH session open.

  .. code-block:: console

    sudo yum install tmux

4.3. Installing Python 3.12
---------------------------
| Code written for this project has been developed using Python 3.12.8.
| Depending on your system, you may need to install Python 3.12 manually (my image comes with 3.6.8).
| Check your installed version with **python3 --version**.
| If you need to install Python 3.12, follow the steps below.
|
| Adapted from `tutorial <https://medium.com/@donfiealex/boost-your-python-installing-3-12-on-centos-7-04c8cdc5dd8f>`_.

1. Install the required dependencies.

  .. code-block:: console
    
    sudo yum install -y gcc openssl-devel bzip2-devel libffi-devel wget

2. Download and install Python 3.12.

  .. code-block:: console

    cd /tmp
    wget https://www.python.org/ftp/python/3.12.8/Python-3.12.8.tgz
    tar xzf Python-3.12.8.tgz

3. Compile and install Python 3.12.

  .. code-block:: console

    cd Python-3.12.8
    ./configure --enable-optimizations
    make
    sudo make install

4. Verify the installation.

  .. code-block:: console

    python3 --version

5. Clean up.

  .. code-block:: console

    cd ..
    sudo rm -rf Python-3.12.8 Python-3.12.8.tgz

6. (Optional) Register Python3.12 as a lower priority, to avoid conflicts with the system Python version.
  - Check existing Python version's priority.

    .. code-block:: console

      alternatives --display python3

  - Register Python3.12 as an alternative. In this example, number 1 is the priority, should be lower than the system Python version's priority.

    .. code-block:: console

      sudo alternatives --install /usr/bin/python3 python3 /usr/local/bin/python3.12 1

4.4. Setting up Java (Minecraft)
--------------------------------
| Java is required to run a Minecraft Server.
| Different versions of minecraft require different versions of minecraft, for example 
| 1.19.4 requires Java SE 17 or newer, whereas 1.21.4 requires Java SE 21 or newer.
| Some versions also cannot use too high of a version, for example 1.19.4 breaks with Java 21.
| This guide will show you how to install Java 21, but you can change Java version according to your server version.
|
1. Install Java 21.

  .. code-block:: console

    sudo yum install java-21-openjdk

2. Verify the installation.

  .. code-block:: console

    java --version

3. (Optional) Set Java <version number> as the default Java version, if multiple versions are installed.

  .. code-block:: console

    sudo update-alternatives --config 'java'

  Select the number corresponding to Java <version number>.

4.5. Setting up Mono (Terraria)
-------------------------------
| Mono is required to run a Terraria Server on Linux arm64 architecture.
|
1. Install the Mono repository.

  .. code-block:: console

    sudo yum install mono-complete

2. If this doesn't work, try the following command and repeat step 1 after completion:

  .. code-block:: console

    sudo tee /etc/yum.repos.d/ol8-epel.repo > /dev/null <<'EOF'
    [ol8_developer_EPEL]
    name=Oracle Linux \$releasever EPEL (\$basearch)
    baseurl=https://yum.oracle.com/repo/OracleLinux/OL8/developer/EPEL/\$basearch/
    gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-oracle
    gpgcheck=1
    enabled=1
    EOF

3. Verify the installation.

  .. code-block:: console

    mono --version
