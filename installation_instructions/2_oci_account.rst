Chapter 2: OCI Account
======================
- `2.1. The Free Tier`_
- `2.2. Pay As You Go (PAYG)`_
- `2.3. Creating an Oracle Cloud Infrastructure Account`_

2.1. The Free Tier
------------------
| `✨About Free Tier✨ <https://docs.oracle.com/en-us/iaas/Content/FreeTier/freetier_topic-Always_Free_Resources.htm>`_
| 
| Oracle Cloud Infrastructure offers an "Always Free" tier which provides a number of services at no cost. ❤
| We are interested in a few resources:

1. Compute
~~~~~~~~~~
Details
^^^^^^^
- All tenancies get a set of Always Free resources in the Compute service for creating compute virtual machine (VM) instances. 
- You must create the Always Free compute instances in your home region.

Our Use Case
^^^^^^^^^^^^
- We make use of the **OCI Ampere A1 Compute instances** for our Minecraft server.
- You are allowed **3000 OCPU hours and 18000 GB hours per month**, which equates to **4 OCPUs and 24 GB of memory** when run 24/7.

2. Compute Reclamation
~~~~~~~~~~~~~~~~~~~~~~
Details
^^^^^^^
- Idle Always Free compute instances may be reclaimed by Oracle. 
- Oracle will deem virtual machine and bare metal compute instances as idle if, during a 7-day period, the following are true:

  - CPU utilization for the 95th percentile is less than 20%
  - Network utilization is less than 20%
  - Memory utilization is less than 20% (applies to A1 shapes only) (we use A1 shapes)

Our Use Case
^^^^^^^^^^^^
- We will assume we are setting a up a Minecraft server.
- We use **2 OCPUs and 12 GB of memory** for our Minecraft server.
- Our server runs 24/7, averaging **21%-25% CPU utilisation** and **50% memory utilisation** (Your mileage may vary...).
- CPU utilisation spikes to **100%** during server reboot.

- I can't find any information on what Oracle uses to measure network utilisation... The following are my assumptions:

  - `About Compute Shapes <https://docs.oracle.com/en-us/iaas/Content/Compute/References/computeshapes.htm#vmshapes>`_
  - According to this page, the A1 shapes have a **1 Gbps network bandwidth per OCPU**.
  - Therefore, to be considered inactive, we would need to use less than **200 Mbps per OCPU** of network bandwidth.

- Network utilisation rates of the server fluctate, but you'd be hard pressed to reach that level of constant network utilisation.
- However, the server doesn't seem to be reclaimed... ¯\\_(ツ)_/¯
- If you don't need this much memory, you could consider using **1 OCPU and 6 GB of memory** instead.

  - My server needs quite a bit of RAM... (✿◡‿◡)

3. Block Volume
~~~~~~~~~~~~~~~
Details
^^^^^^^
| `About Block Volume <https://docs.oracle.com/en-us/iaas/Content/Block/Concepts/overview.htm>`_
|
- All tenancies receive a total of 200 GB of Block Volume storage included in the Always Free resources. 
- These amounts apply to both boot volumes and block volumes combined.
|
- A boot volume is a detachable device that contains the image used to boot the compute instance.
- A detachable block storage device that allows you to dynamically expand the storage capacity of an instance.

Our Use Case
^^^^^^^^^^^^
- We make use of the default boot volume size of **47 GB** for our server.
- We do not require additional block volumes.
- As long as the total storage used by both boot and block volumes does not exceed 200 GB, no additional charges will be incurred.
- Even if the instance cost calculator states `otherwise <https://www.reddit.com/r/oraclecloud/comments/14pg5dr/oracle_always_free_service_have_boot_volume_cost/>`_, no charges will be incurred as long as the total storage used does not exceed 200 GB.

4. Outbound Data Transfer
~~~~~~~~~~~~~~~~~~~~~~~~~
Details
^^^^^^^
- All tenancies receive 10 TB of outbound data transfer per month for Always Free resources.

Our Use Case
^^^^^^^^^^^^
- We do not expect to exceed this limit. (°ー°〃)

  - 4 TB = 10995116277760 B
  - Seconds in a 31 day month = 60 * 60 * 24 = 2678400
  - Must Exceed 10995116277760 B / 2678400 s = 4105106.14 B/s
  - Must Exceed 4105106.14 B/s / 1024 / 1024 = **3.91 MB/s NONSTOP I/O**

2.2. Pay As You Go (PAYG)
-------------------------
| Nothing in life is truly free... or is it?
| When I first started the free-trial, everything worked fine. Until about 1 month in.
| Oracle decided to reclaim the instance without warning, and I had to recreate the instance from scratch.
| However, no matter how often you try to recreate the instance, you will not be able to due to "insufficient capacity".
|
| According to this `reddit thread <https://www.reddit.com/r/selfhosted/comments/15q1o59/is_oracle_cloud_free_tier_actually_free_tier/>`_, VMs under the free tier are easily get flagged as not in use.
| Additionally, free tier accounts use a separate hardware allocation pool from Pay As You Go (PAYG) accounts.
| According to a few users, free tier accounts can take weeks to get a VM, whereas PAYG has always been instant for them.
| 
| In conclusion, the free tier is great for testing, but you may find yourself needing to update to PAYG if you don't want any hiccups.
| Once logged into the management console, see your payment details `here <https://cloud.oracle.com/invoices-and-orders/upgrade-and-payment>`_.
| You can choose to upgrade your account to PAYG, which will require you to enter your payment details.
| Remember that as long as you don't exceed the free tier limits, you won't be charged.

2.3. Creating an Oracle Cloud Infrastructure Account
----------------------------------------------------
| Sign up and Login here: `OCI Sign In <https://www.oracle.com/cloud/sign-in.html>`_.
| Credit card details must be provided, but the account remains in the free tier until you explicitly upgrade to PAYG.
