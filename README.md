EPSCOR_Bramble_GH9C
===================

## A cluster of Raspberry PIs is generally referred to as a bramble. ##

## Information about the project ##
  * Raspberry PI:
      * 180 Raspberry PIs (rPIs) on a gantry above the greenhouse.
      * Powered by rPI adapters plugged into power strips.
          * Make sure there is no electromagnetic interference by assuring no loops in the power cables.
      * One Raspberry PI (omegabackup) kept outside with monitor and keyboard for quick maintenance.
      * One Raspberry PI (alphabackup) kept for testing new scripts to be sent to rPIs.
      * One Raspberry PI (serverpi) kept to be the server for [ganglia](http://ganglia.info/) -- It collects data from the bramble and transmists it to a ganglia host which allows a broad overview of rPI load, uptime, etc. over a given time interval.
      * Ganglia screenshot:
      
![Screenshot of Ganglia](screenshots/Ganglia-Screenshot.PNG)

  * Two Wireless Access Points (WAP) specifically dedicated to the bramble and two others simulcasting for a total of 4 SSIDs to subdivide the bramble. Approximately 45 rPIs per WAP.
  * Because of current location there is a lot of wireless interference so the rPIs have their transmit power turned down to 18 db at all times. It is increased back up to 20 db before copying files over.
  * The interference at the moment doesn't allow for more than about 165 rPIs to be able to be functioning at the same time for most wireless transfers. The cron jobs on the bramble will manage taking pictures, however, the centralized server must be in charge of copying pictures to storage so as to be able to manage the bramble.
  * The bramble is managed from a centralized server on the infrastructure using [Ansible](https://www.ansible.com/), a [configuration/deployment IT management engine](https://en.wikipedia.org/wiki/Ansible_(software)) written in Python.

## Initial Setup ##
  * Raspberry PI Setup:
      * Load the latest version of debian onto the rPIs.
      * Configure each rPI with their own hostname, WiFi access, IP address (if static), etc.
          * This repo has bash files in [pi_config](pi_config) that I used for fast configuration of the Raspberry PI. They are very specific to our configuration, but if you want to use them as an idea of how to more quickly configure rPIs please take a look.
          * The debian version used is Raspbian GNU/Linux 8 (jessie) for these scripts.
      * At minimum before Ansible can work with the rPIs, they need an openssh-server (`sudo apt-get install openssh-server`); a unique hostname, IP address, or both; ssh keys from the centralized server copied onto them; and a user.
      * The preferred method is to configure one rPI with all of the settings which are the same across the entire bramble and then clone that image using any of the [available methods](http://www.htpcguides.com/easy-resize-and-back-up-raspberry-pi-sd-card-with-ubuntu/).
  * Centralized server setup:
      * Generate ssh-key for user that will interact with the bramble.
          * `ssh-copy-id` will be the preferred command to copy keys.
          * If automating, install and use `sshpass` to use the default rPI password without having to input it 180 times.
      * Install Ansible using their documentation.
          * If you want to use more advanced rsync options (i.e. rsh, controlmaster on rsync) then change the synchronize.py file with the one in the repo after changing the options in it. Use at your own risk.
      * Use the playbooks (.yml files) here after setting up your ansible!
      * The hosts file will need to be changed entirely to match your setup.
      
## Ansible Playbooks and Bash Script ##

