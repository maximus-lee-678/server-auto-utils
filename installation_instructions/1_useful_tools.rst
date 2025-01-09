Section 1: Useful Tools
=======================
- `1.1. PuTTY`_
- `1.2. WinSCP`_

1.1. PuTTY
----------
SSH client of choice, allows for access to created Oracle Cloud instance.

Installation
~~~~~~~~~~~~
Download and install PuTTY from their `website <https://www.putty.org/>`_.

Usage
~~~~~
| Adapted from `tutorial <https://devops.ionos.com/tutorials/use-ssh-keys-with-putty-on-windows/>`_.
| 
#. During the creation of an Oracle Cloud instance, a public and private key will be generated (.key.pub and .key).
#. Launch PuTTYgen.
#. Click Conversions from the PuTTY Key Generator menu and select Import key.
#. Navigate to the OpenSSH private key and click Open.
#. Under Actions / Save the generated key, select Save private key.
#. Choose an optional passphrase to protect the private key.
#. Save the private key (.ppk).
#. The PuTTYgen tool can be closed.
#. Launch PuTTY.
#. Enter the remote server Host Name or IP address under Session, and ensure connection type is set to SSH.
#. Navigate to Connection > SSH > Auth.
#. Click Browse... under Authentication parameters / Private key file for authentication.
#. Locate the id_rsa.ppk private key and click Open.
#. Navigate to Connection > Data.
#. Specify the Auto-login username under Login details as "opc".
#. Navigated back to Session and save the session by entering a name under Saved Sessions and clicking Save.
#. Finally, click Open to log into the remote server.

1.2. WinSCP
-----------
| SFTP client of choice, allows for easy file transfer to and from the created Oracle Cloud instance.
| Of course, if you don't want to use an SFTP client, you can always use wget! :)

Installation
~~~~~~~~~~~~
Download and install WinSCP from their `website <https://winscp.net/eng/download.php>`_.

Usage
~~~~~
If PuTTY has already been set up and initialised, WinSCP can import configured authentication details directly.
