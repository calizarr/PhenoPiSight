PhenoPiSight
===================

EPSCOR_Bramble_GH9C
-------------------


In this documentation, we outline the management of 165 Raspberry Pis currently deployed and wirelessly maintained in Greenhouse 9C at the Donald Danforth Plant Science Center. Also included is our current pipeline for image analysis using VisualSFM.

## A cluster of Raspberry PIs is generally referred to as a bramble. ##

## Information about the project ##

### Raspberry PI ###
  * 165 Raspberry PIs (rPIs) on a gantry above the greenhouse
  * Powered by rPI adapters plugged into power strips and wireless internet access is provided via WiFi dongles
  * Make sure there is no electromagnetic interference by assuring no loops in the power cables
  * One Raspberry PI (omegabackup) kept outside with monitor and keyboard for quick maintenance
  * One Raspberry PI (alphabackup) kept for testing new scripts to be sent to rPIs
  * One Raspberry PI (serverpi) kept to be the server for [Ganglia][] -- It collects data from the bramble and transmists it to a ganglia host which allows a broad overview of rPI load, uptime, etc. over a given time interval
  * **Ganglia**
      * Ganglia screenshot:  
      * ![Screenshot of Ganglia][]  
      * **Ganglia is entirely optional.**
  * **Wireless Access Points**
      * Two Wireless Access Points (WAP) specifically dedicated to the bramble and two others simulcasting for a total of 4 SSIDs to subdivide the bramble. Approximately 45 rPIs per WAP
      * Because of current location there is a lot of wireless interference so the rPIs have their transmit power turned down to 18 db at all times. It is increased back up to 20 db before copying files over
      * The interference at the moment doesn't allow for more than about 165 rPIs to be able to be functioning at the same time for most wireless transfers. The cron jobs on the bramble will manage taking pictures, however, the centralized server must be in charge of copying pictures to storage so as to be able to manage the bramble
  * **Bramble Management**
      * The bramble is managed from a centralized server on the infrastructure using [Ansible][], a [configuration/deployment IT management engine][] written in Python
### Raspberry PI Physical Location ###
The grid for the Raspberry Pis/Bramble looks like this in both:  
**Octet Format** and **Coord Format**
<p float="left">
<img src="https://github.com/calizarr/EPSCoR_Bramble_GH9C/blob/master/screenshots/rpi_grid_octet.png" alt="Octet Format" width="370" height="526" \>
<img src="https://github.com/calizarr/EPSCoR_Bramble_GH9C/blob/master/screenshots/rpi_grid_coord.png" alt="Coord" width="370" height="526" \>
 </p>  
 
  * The perspective of the images is from the door entering the greenhouse on the bottom left near 10.9.0.16 (30,1)
  * The Octet format is the IP address of every rPI starting with 10.9.0.11 from the bottom right to 10.9.0.190 on the top left
  * The Coord format is the translated matrix coordinates of the last octet of the IP address (11 for 10.9.0.11) reversed in order (from 11 top left to 190 bottom right)
  * The last octet is treated as a 1 dimensional data structure representing a 2 dimensional grid
  * 1D representation: `[0, 1, 2, 3]`
  * 2D representation:
    * `[0,0 0,1]`
    * `[1,0 1,1]`
    * `[y,x]`
  * The formulas are:
    * i is the sequential representation, x is the x coordinate in grid form, y is the y coordinate in grid form, width is the width of the matrix aka the length of the x-axis
    * `x = i % width`
    * `y = i / width ;; integer division`
    * `i =  x + width * y`
    * More information can be found [here][]
  * The colors represent the division of rPIs per Wireless Access Point

[here]: http://programmers.stackexchange.com/questions/212808/treating-a-1d-data-structure-as-2d-grid

## For more in-depth installation instructions visit the [Installation, setup, and user guide][] ##

[Installation, setup, and user guide]: Installation_guide.md

## Initial Setup ##

### Requirements ###
  * *N* number of Raspberry Pis (rPIs)
      * Each rPI should have a camera module and a WiFi dongle
      * We use the [WiPi Dongle][]
          * Allows transmit power changes without reboot
          * More powerful than Adafruit dongles
      * Each rPI should have its own case
  * Centralized Linux server/desktop to run Ansible
      * Networked and able to connect to the rPIs
      * Must be on 24/7
      * Must have enough storage space to store images
      * [Ansible Requirements][]
      
[Ansible Requirements]: http://docs.ansible.com/ansible/intro_installation.html#control-machine-requirements

[WiPi Dongle]: https://www.element14.com/community/docs/DOC-69361/l/wifi-usb-dongle-for-raspberry-pi

### Centralized server setup / Ansible setup ###
  * Generate ssh-key for user that will interact with the bramble
      * `ssh-copy-id` is the best command to copy keys. It is usually installed with openssh
      * The idea is to copy the ssh key to the rPI that will be used to make the image that will be restored for all the other rPIs
  * Install Ansible using [their documentation][]
      * If you want to use more advanced rsync options (i.e. rsh, controlmaster on rsync) then change the synchronize.py file with the one in the repo after changing the options in it
      *  *Use at your own risk. rsh is insecure, and controlmaster may affect performance negatively depending on your setup.*

[their documentation]: http://docs.ansible.com/ansible/intro_installation.html

### Raspberry PI Setup ###
  * Load the latest version of [debian/raspbian onto the rPIs.][]
  * Configure each rPI with their own hostname, WiFi access, IP address (if static), camera module, timezone, etc
      * This repo has bash files in [pi_config](pi_config) that I used for fast configuration of the Raspberry PI. They are very specific to our configuration, but if you want to use them as an idea of how to more quickly configure rPIs please take a look. **Use these scripts at your own risk**
          * The debian version used is Raspbian GNU/Linux 8 (jessie) for these scripts
   * At minimum before Ansible can work with the rPIs, they need an openssh-server (`sudo apt-get install openssh-server`); a unique hostname, IP address, or both; ssh keys from the centralized server copied onto them; and a user
      * The preferred method is to configure one rPI with all of the settings which are the same across the entire bramble and then clone that image using any of the [available methods][]

[debian/raspbian onto the rPIs.]: https://www.raspberrypi.org/downloads/raspbian/

### Managing Bramble with Ansible ###
  * The [hosts file / Ansible inventory][] will need to be changed entirely to match your setup
  * The [configuration file][] will also need to be changed to match your setup or not changed at all
  * Modify the [Ansible playbooks][] to work for your setup
      * [Ansible Playbooks Documentation][]
  * The playbook-ansible bash script takes logs with timestamps and retries at least three times with increasing timeouts
      * Make sure to modify it for your environment if you will be using it

[hosts file / Ansible inventory]: http://docs.ansible.com/ansible/intro_inventory.html

[configuration file]: http://docs.ansible.com/ansible/intro_configuration.html

[Ansible Playbooks Documentation]: http://docs.ansible.com/ansible/playbooks_intro.html

[Ansible playbooks]: playbooks/

### Image Storage ###
  * The images are stored on the centralized Ansible server that copies the pictures using the playbooks

## For more in-depth installation instructions visit the [Installation, setup, and user guide][] ##
      
## Things to Know Before Embarking on a Bramble Adventure ##
  * [How To Install An Image Onto A Raspberry Pi][]
  * [General Raspberry Pi Documentation][]
  * [GitHub Introduction][]

[Screenshot of Ganglia]: screenshots/Ganglia-Screenshot.PNG "Ganglia Screen"
[Ganglia]: http://ganglia.info/ "Ganglia Homepage"
[Ansible]: https://www.ansible.com/ "Ansible Homepage"
[configuration/deployment IT management engine]: https://en.wikipedia.org/wiki/Ansible_(software) "Wikipedia on Ansible"
[available methods]: http://www.htpcguides.com/easy-resize-and-back-up-raspberry-pi-sd-card-with-ubuntu/

[How To Install An Image Onto A Raspberry Pi]: https://www.raspberrypi.org/documentation/installation/installing-images/

[General Raspberry Pi Documentation]: https://www.raspberrypi.org/documentation/

[GitHub Introduction]: https://guides.github.com/activities/hello-world/

