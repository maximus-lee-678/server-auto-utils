Chapter 3: Oracle Instance Creation
===================================
| Instructions largely transcribed from this `oracle blog post <https://blogs.oracle.com/developers/post/how-to-set-up-and-run-a-really-powerful-free-minecraft-server-in-the-cloud>`_.
| There's pictures on there, you should visit it!
| This section assumes you have an Oracle Cloud Infrastructure account ready and are logged in.
|
1. Create a VM instance. Can be done by searching "Instances" in the search bar and selecting "Create Instance".
2. Specify an instance name and compartment name (optional).
3. "Placement" and "Security settings can left as default.
4. Under "Image and shape", change the image to "Oracle Linux 7.9".
5. Under "Image and shape", select shape series "Ampere" and select the shape "VM.Standard.A1.Flex".
6. Configure the number of OCPUs and memory. As long as totals don't exceed 4 OCPUs and 24 GB of memory, no charges will be incurred.
7. Under "Primary VNIC information", create a new virtual cloud network and subnet in your compartment.
8. If you have an existing VCN, you can select it from the dropdown.
9. CIDR block can be left as default, and make sure "Automatically assign private IPv4 address" and "Automatically assign public IPv4 address" are checked.
10. Under "Add SSH keys", generate a new SSH key pair. MAKE SURE YOU SAVE THESE KEYS BY DOWNLOADING THEM.
11. Leave boot and block volume defaults and click 'Create".
12. As soon as you click "Create", you'll be redirected to the VM details page and your VM instance will be in a "PROVISIONING" state.
13. After a while, the state will switch to "RUNNING". Find your public IP address and copy it.
14. SSH into your instance using the generated keys as the **opc** user. How to connect? See Section 1.1.
15. After verifying the instance works, navigate back to the VM details page.
16. Under "Instance Information", find "Primary VNIC" and click on the subnet link.
17. Click on the default "Security List".
18. Click "Add Ingress Rules" and add the following rules:
19. Add 2 Ingress Rules - one for TCP and one for UDP - each with a "Source CIDR" of 0.0.0.0/0 and a destination port range of 25565.
20. Back in the SSH session, run the following commands to open these ports on the VM's firewall:

.. code-block:: console

  sudo firewall-cmd --permanent --zone=public --add-port=25565/tcp
  sudo firewall-cmd --permanent --zone=public --add-port=25565/udp
  sudo firewall-cmd --reload

21. Ready to go!
