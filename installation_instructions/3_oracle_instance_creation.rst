Chapter 3: Oracle Instance Creation
===================================
| Instructions largely transcribed from this `oracle blog post <https://blogs.oracle.com/developers/post/how-to-set-up-and-run-a-really-powerful-free-minecraft-server-in-the-cloud>`_.
| There's pictures on there, you should visit it!
| This section assumes you have an Oracle Cloud Infrastructure account ready and are logged in.
|
| I HIGHLY RECOMMEND AGAINST ANYTHING OLDER THAN ORACLE LINUX 9. THE VERSION OF GLIBC ON ORACLE LINUX 8 IS 2.28, AND JAVA 25 REQUIRES GLIBC 2.29+.
| IF YOU PLAN ON USING JAVA 25 (Hytale, Minecraft version 26+), HEED MY WARNING, DON'T WASTE HOURS LIKE I DID, JUST USE ORACLE LINUX 9+.
|
| `Oracle Linux 8 <https://docs.oracle.com/en/operating-systems/oracle-linux/8/relnotes8.0/OL8-RELNOTES8-0.pdf>`_ has **glibc 2.28** and **python3.6**.
| `Oracle Linux 9 <https://docs.oracle.com/en/operating-systems/oracle-linux/9/relnotes9.0/OL9-RELNOTES-9-0.pdf>`_ has **glibc 2.34** and **python3.9**.
| `Oracle Linux 10 <https://docs.oracle.com/en/operating-systems/oracle-linux/10/relnotes10.0/OL10-RELNOTES-10-0.pdf>`_ has **glibc 2.39** and **python3.12**.
|
| Although the blog post details instructions for creation of a Minecraft server, the instructions here are general and can be used for other game servers as well.
|
| Incoming wall of text!
|
1. Create a VM instance. Can be done by searching "Instances" in the search bar and selecting "Create Instance".
2. **[Stage 1]** Specify an instance name (better change it to something good) and compartment name (optional).
3. "Placement" values can left as default.
4. Under "Image", change the image to "Oracle Linux 10". (important to use 9+ if you want to run a Hytale or Minecraft version 26+ server.)
5. Under "Shape", select shape series "Ampere" and select the shape "VM.Standard.A1.Flex".
6. By clicking the small arrow next to the shape name, you can configure the number of OCPUs and memory. As long as totals don't exceed 4 OCPUs and 24 GB of memory, no charges will be incurred.
7. **[Stage 2]** "Security" values can left as default.
8. **[Stage 3]** Specify your VNIC name.
9. Under "Primary network", create a new virtual cloud network and subnet in your compartment.
10. If you have an existing VCN and subnet, you can select them from their respective dropdowns.
11. Under Private IPv4 Assignment, and make sure "Automatically assign private IPv4 address" is selected.
12. Under Public IPv4 Assignment, and make sure "Automatically assign public IPv4 address" is selected.
13. No need to change Networking advanced options.
14. Under "Add SSH keys", choose "Generate a key pair for me". MAKE SURE YOU SAVE THESE KEYS BY DOWNLOADING THEM.
15. **[Stage 4]** Leave boot and block volume defaults.
16. **[Review]** Verify entered details are correct.
17. As soon as you click "Create", you'll be redirected to the instance details page and your instance will be in a "PROVISIONING" state.
18. After a while, the state will switch to "RUNNING". Find your public IP address and copy it.
19. SSH into your instance using the generated keys as the **opc** user. How to connect? See Section 1.1.
20. After verifying the instance works, navigate back to the instance details page.
21. Under the "Networking" tab, find the "Attached VNICs" section and click on the the "Primary VNIC's" corresponding "Subnet/VLAN link" link.
22. Under the "Security" tab, click on the "Default Security List".
23. Under the "Security Rules" tab, click "Add Ingress Rules" and add the following rules FOR EACH GAME SERVER PORT YOU WANT TO OPEN (e.g. Minecraft uses 25565 by default):
24. Add 2 Ingress Rules - one for TCP and one for UDP - each with a "Source CIDR" of 0.0.0.0/0 and a single destination port of your choice.
25. Back in the SSH session, run the following commands to open the same ports on the VM's firewall (replace <port_no> with your chosen port number(s)):

.. code-block:: console

  sudo firewall-cmd --permanent --zone=public --add-port=<port_no>/tcp
  sudo firewall-cmd --permanent --zone=public --add-port=<port_no>/udp
  sudo firewall-cmd --reload

26. Example (defaults for Minecraft, Terraria, Hytale):

.. code-block:: console

  sudo firewall-cmd --permanent --zone=public --add-port=25565/tcp
  sudo firewall-cmd --permanent --zone=public --add-port=25565/udp
  sudo firewall-cmd --permanent --zone=public --add-port=7777/tcp
  sudo firewall-cmd --permanent --zone=public --add-port=7777/udp
  sudo firewall-cmd --permanent --zone=public --add-port=5520/tcp
  sudo firewall-cmd --permanent --zone=public --add-port=5520/udp
  sudo firewall-cmd --reload

27.  Good to go!
