==============================
Legacy Bash Automation Scripts
==============================

These files are so old, even the README isn't formatted! :p

This directory contains a bunch of bash scripts written to automate backups and reboots. These were written very hastily (like 1 day if I recall), and as such are not written very well and may contain bugs. There is also no global declaration of variables, and strings are repeated across multiple files, making updates difficult. This process in now simplified with the .env file.

There are also mentions of a "gdrive_path". This refers to a third-party binary that allows interfacing with Google Drive, known as gdrive2. The repository for this code can be found at https://github.com/prasmussen/gdrive/. As of writing, this project is no longer maintained and Google has changed their requirements to interact with Google Drive. In the present, since we have moved to Python as the preferred language for these utilities, we instead make use of the PyDrive2 library to fulfil our Google Drive operations.

A fun (?) fact, you may have gleaned from these scripts that the minecraft server is commonly referred to as "skyblock_1.19", which was the original use case of these utilities. 🌃🌇

There are also a few caveats with the crontab configuration, the most glaring being that the restart capability has never worked, as sudo reboot cannot be issued by a non-root cronjob (I only realised this recently...) (skill issue). Another issue is that commands are always triggered at predefined times, instead of being chained and reboot driven. This causes restart events to take longer and also potentially miss a step.

As such, these scripts are no longer actively being used, with the new Python scripts being favoured instead. (✿◡‿◡)
