EPSCOR_Bramble_GH9C
===================

## A cluster of Raspberry PIs is generally referred to as a bramble. ##

## Information about the project ##

### Raspberry PI: ###
  * 180 Raspberry PIs (rPIs) on a gantry above the greenhouse.
  * Powered by rPI adapters plugged into power strips.
  * Make sure there is no electromagnetic interference by assuring no loops in the power cables.
  * One Raspberry PI (omegabackup) kept outside with monitor and keyboard for quick maintenance.
  * One Raspberry PI (alphabackup) kept for testing new scripts to be sent to rPIs.
  * One Raspberry PI (serverpi) kept to be the server for [Ganglia][] -- It collects data from the bramble and transmists it to a ganglia host which allows a broad overview of rPI load, uptime, etc. over a given time interval.
  * **Ganglia**
      * Ganglia screenshot:  
      * ![Screenshot of Ganglia][]  
      * **Ganglia is entirely optional.**
  * **Wireless Access Points**
      * Two Wireless Access Points (WAP) specifically dedicated to the bramble and two others simulcasting for a total of 4 SSIDs to subdivide the bramble. Approximately 45 rPIs per WAP.
      * Because of current location there is a lot of wireless interference so the rPIs have their transmit power turned down to 18 db at all times. It is increased back up to 20 db before copying files over.
      * The interference at the moment doesn't allow for more than about 165 rPIs to be able to be functioning at the same time for most wireless transfers. The cron jobs on the bramble will manage taking pictures, however, the centralized server must be in charge of copying pictures to storage so as to be able to manage the bramble.
  * **Bramble Management**
      * The bramble is managed from a centralized server on the infrastructure using [Ansible][], a [configuration/deployment IT management engine][] written in Python.
  * **Raspberry PI Physical Location**
      * The grid for the Raspberry Pis/Bramble looks like this in both:
          * **Octet Format** and **Coord Format**  
          <img src="https://github.com/calizarr/EPSCOR_Bramble_GH9C/blob/master/screenshots/rpi_grid_octet.png" align="left" width="370" height="526">
          <img src="https://github.com/calizarr/EPSCOR_Bramble_GH9C/blob/master/screenshots/rpi_grid_coord.png" align="right" width="370" height="526"><br/>  
      * The perspective of the images is from the door entering the greenhouse on the bottom left near 10.9.0.16 (30,1)
      * The Octet format is the IP address of every rPI starting with 10.9.0.11 from the bottom right to 10.9.0.190 on the top left.
      * The Coord format is the translated matrix coordinates of the last octet of the IP address (11 for 10.9.0.11) reversed in order (from 11 top left to 190 bottom right).
      * The last octet is treated as a 1 dimensional data structure representing a 2 dimensional grid.
          * 1D representation: `[0, 1, 2, 3]`
          * 2D representation:
          * `[0,0 0,1]`
          * `[1,0 1,1]`
          * `[y,x]`
          * The formulas are:
              * i is the sequential representation, x is the x coordinate in grid form, y is the y coordinate in grid form, width is the width of the matrix aka the length of the x-axis.
              * x = i % width
              * y = i / width ;; integer division
              * i =  x + width * y
          * More information can be found [here][]
      * The colors represent the division of rPIs per Wireless Access Point

[here]: http://programmers.stackexchange.com/questions/212808/treating-a-1d-data-structure-as-2d-grid

## For more in-depth installation instructions visit the [Installation guide][] ##

[Installation guide]: Installation_guide.md

## Initial Setup ##
  * **Raspberry PI Setup:**
      * Load the latest version of debian onto the rPIs.
      * Configure each rPI with their own hostname, WiFi access, IP address (if static), etc.
          * This repo has bash files in [pi_config](pi_config) that I used for fast configuration of the Raspberry PI. They are very specific to our configuration, but if you want to use them as an idea of how to more quickly configure rPIs please take a look.
          * The debian version used is Raspbian GNU/Linux 8 (jessie) for these scripts.
          * Use at your own risk.
      * At minimum before Ansible can work with the rPIs, they need an openssh-server (`sudo apt-get install openssh-server`); a unique hostname, IP address, or both; ssh keys from the centralized server copied onto them; and a user.
      * The preferred method is to configure one rPI with all of the settings which are the same across the entire bramble and then clone that image using any of the [available methods][].
  * **Centralized server setup:**
      * Generate ssh-key for user that will interact with the bramble.
          * `ssh-copy-id` will be the preferred command to copy keys.
          * If automating, install and use `sshpass` to use the default rPI password without having to input it 180 times.
      * Install Ansible using their documentation.
          * If you want to use more advanced rsync options (i.e. rsh, controlmaster on rsync) then change the synchronize.py file with the one in the repo after changing the options in it.
          *  Use at your own risk.
      * Use the [playbooks (.yml files) here](playbooks) after setting up your ansible!
      * The hosts file will need to be changed entirely to match your setup.
      
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

