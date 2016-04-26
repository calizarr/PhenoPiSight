Installation, setup, and user guide
===================================

### Getting Started ###
  * Raspberry Pis will require some usage of the Linux terminal and it's worth knowing how to get around a bit. The Raspberry Pi foundation provides a [quick tutorial][].
  * As great as it is, it does not give you information on how to use `nano` the default Linux text editor:
      * [Beginnner's Guide to Nano][]
      * [Nano Basics][]
  * Many of the Raspberry Pi camera commands can be better used with the Python library included with Raspbian. The Raspberry Pi foundation also provides a [quick python tutorial][].
  * Feel free to refer back to these links as you go through the installation steps for the Raspberry Pi.
  * Also, when instructions are surrounded in brackets `<>` such as `<YourInputHere>` type your particular name or folder name there without the brackets.
  * You will also need an introduction to GitHub to clone and use this repository.
      * GitHub primer to get you started: [GitHub Introduction: Hello World!][]
  * To clone this GitHub repository: 
      * Type or copy/paste: `git clone git@github.com:calizarr/EPSCOR_Bramble_GH9C.git` to clone this repository into a folder named EPSCOR\_Bramble\_GH9C.
      * If you want to clone it into a different folder name, type: `git clone git@github.com:calizarr/EPSCOR_Bramble_GH9C.git <YourFolderName>`

[quick tutorial]: https://www.raspberrypi.org/documentation/usage/terminal/README.md

[Beginnner's Guide to Nano]: http://www.howtogeek.com/howto/42980/the-beginners-guide-to-nano-the-linux-command-line-text-editor/

[Nano Basics]: https://wiki.gentoo.org/wiki/Nano/Basics_Guide

[quick python tutorial]: https://www.raspberrypi.org/documentation/usage/python/README.md

[GitHub Introduction: Hello World!]: https://guides.github.com/activities/hello-world/

### Requirements ###
  * *N* number of Raspberry Pis (rPIs)
      * Each rPI should have a camera module and a WiFi dongle.
      * We use the [WiPi Dongle][].
          * Allows transmit power changes without reboot.
          * More powerful than Adafruit dongles.
  * Centralized Linux server/desktop to run Ansible.
      * Networked and able to connect to the rPIs.
      * Must be on 24/7
      * [Ansible Requirements][]

[Ansible Requirements]: http://docs.ansible.com/ansible/intro_installation.html#control-machine-requirements

[WiPi Dongle]: https://www.element14.com/community/docs/DOC-69361/l/wifi-usb-dongle-for-raspberry-pi

### Ansible Setup ###
  * Depending on the setup of the centralized server that will be launching Ansible, you will need to pick what is best for you from the [Ansible installation documentation][].
  * We installed ansible from github for a rootless (no privileges) installation.
      * If installed on a server infrastructure, if you do not have access to an administrator or administrator privileges, a github installation may be the best option for you.
  * Ansible setup is rather straightforward and should not be very problematic.
  * After you have installed Ansible on your server, make sure to generate ssh keys for the server.
      * [GitHub Generating SSH-Key][]
      * [Digital Ocean SSH Key Tutorial][]
          * Don't disable password for root login.

[Ansible installation documentation]: http://docs.ansible.com/ansible/intro_installation.html

[GitHub Generating SSH-Key]: https://help.github.com/articles/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent/

[Digital Ocean SSH Key Tutorial]: https://www.digitalocean.com/community/tutorials/how-to-set-up-ssh-keys--2

### Raspberry Pi Setup ###
  * [Raspberry PI Quick Start Guide][]
  * First, we need to install an operating system onto the Original Raspberry Pi sd card.
  * **Follow this documentation:** [Raspberry Pi Installing Operating Systems][]
  * [Debian jessie][] is the recommmended raspbian distribution.
  * ***To avoid problems in the future, make sure that your SD card used for cloning is the smallest SD card you have. Even if they claim to be of the same size -- 8 GBs is not the same across all SD cards.***
      * In these examples, I am using an 8 GB sd card.
      * Linux Terminal: Open a terminal, type or copy/paste `df -h`, and look at the  `/dev/root` Filesystem and its `Size` parameter.
      * ![size_screenshot][]
      * Windows: Go into Windows Explorer, Right click the SD card drive, go to properties, and check the capacity.
          * ![windows_explorer_capacity][]
          * If it already has a Linux filesystem format, Windows won't be able to read it directly.
          * Instead, press `Win+R` or open a command prompt, then type `diskmgmt.msc` and look for a Disk about the size of your SD card.
          * ![windows_diskmgmt_capacity.png][]
  * Follow all the prompts after installing Raspbian/Debian Jessie onto the Original Raspberry Pi, then continue onward.

[size_screenshot]: screenshots/sd_card_size.png

[windows_explorer_capacity]: screenshots/windows_explorer_capacity.png

[windows_diskmgmt_capacity.png]: screenshots/windows_diskmgmt_capacity.png

[Raspberry Pi Installing Operating Systems]: https://www.raspberrypi.org/documentation/installation/installing-images/

[debian jessie]: https://www.raspberrypi.org/downloads/raspbian/

#### Setting up your Raspberry Pi: ####

  * Log in to the Original Raspberry PI using a usb mouse and keyboard and an HDMI capable monitor.
  * **WiFi:**
      * Set up the network following instructions using the Graphical User Interface (GUI): [GUI WiFi Setup][]
          * Look only under the **New Wifi Interface** heading.
      * If using the command line interface (CLI), follow this set of instructions: [Raspberry PI CLI setup][]
  * **Camera:**
      * [Follow these instructions for enabling and installing the camera.][]
  * **Hostname:**
      * [Change hostname using command line][]
      * Make sure to give your Raspberry PI a unique hostname.
          * Our rPIs hostnames range from ShakoorCamera11 to ShakoorCamera190 so that they do not conflict with each other.
          * We also gave our rPIs static IP addresses ranging from 10.9.0.11 to 10.9.0.190.
          * Given the density of our bramble we had to provide static IP addresses, but it may not be necessary otherwise.
          * Static IP Addresses are a bit more complicated but they are documented [here][].
              * The previous GUI WiFi Setup also includes information on how to set up static IP addresses via the GUI.
          * Also take a look at the file in [pi_config/dhcpcd.conf][] for an idea of what to put in your dhcpcd.conf
              * Most of it is default boilerplate, the important section for static IP addresses starts at line 43.
              * Your `domain_name_servers`, `ip_address`, `routers`, and `hostname` will be different
  * **Wireless Power Management:**
      * Open a terminal:
          * Type or copy/paste: `sudo nano /etc/network/interfaces` in a new line under `wlan0`
          * Type or copy/paste: `wireless-power off`
          * Exit and save the file with nano. (`Ctrl+X -> Y -> Enter`)
          * This removes all wireless power management which prevents random disconnects.
  * **OpenSSH Server**
      * Open a terminal and type or copy/paste: `sudo apt-get install openssh-server`
      * Test the ssh server by logging in with: `ssh pi@localhost`
      * To also test if your hostname works check: `ssh pi@<YourHostnameHere>`
      * Finally, if hostname doesn't work, find your [Raspberry Pi IP address][] and try: `ssh pi@<YourIpAddressHere>`
          * If hostnames don't work, I highly suggest setting up static IP addresses for each rPI to make sure that you know which one you are accessing.
      * To make sure all rPIs have the Ansible server's ssh-key and are a known host, from the Ansible server:
          * Open a terminal and type or copy/paste: `ssh-copy-id pi@<YourHostnameHere>` or `ssh-copy-id pi@<YourIpAddressHere>`
          * *If you don't do this step you will have to copy it individually for every rPI you have later!*
  * **Set the Timezone**
      * Open a terminal and type or copy/paste: `sudo dpkg-reconfigure tzdata`
      * Set your timezone.
      * This will be the timezone of all the rPIs in the bramble.
      * *If you don't do this step you will have to copy it individually for every rPI you have later or use UTC time!*
  * **Playbooks Adjustments**
      * If you will be using the playbooks in this repository, then you need to add a few things on the original rPI.
      * Make a folder for the images:
          * Open a terminal and type or copy/paste: `mkdir /home/pi/Images`
      * Alter the [python camera script][] to suit your needs.
          * Comment out lines 143-144 and uncomment line 145
          * Lines 143-144 look like:  
          `grid = convert_ip(get_ip(), width, height, offset)`  
          `filename = "{hostname}_Y{y}_X{x}_{now}.png".format(hostname=hostname, x=grid[1], y=grid[0], now=now.strftime("%Y-%m-%d-%H-%M"))`  
          * Line 145 looks like: `# filename = hostname+"_"+now.strftime("%Y-%m-%d-%H-%M")+".png"`
      * After altering the script, copy the [python camera script][] to `/home/pi/`
          * You can do it by copying the [python camera script][] to the `/home/pi/` folder in the Raspberry Pi.
          * You could also clone the repository onto the Original Raspberry Pi, alter the script, and then move it to `/home/pi` by opening a terminal then type or copy/paste `mv camera_single.py /home/pi`

[Raspberry Pi IP address]: https://learn.adafruit.com/adafruits-raspberry-pi-lesson-3-network-setup/finding-your-pis-ip-address

[python camera script]: pi_files/camera_single.py

[Raspberry PI CLI setup]: https://www.raspberrypi.org/documentation/configuration/wireless/wireless-cli.md

[Raspberry PI Quick Start Guide]: https://www.raspberrypi.org/help/quick-start-guide/

[GUI WiFi Setup]: https://www.raspberrypi.org/blog/another-raspbian-desktop-user-interface-update/

[Change hostname using command line]: http://www.howtogeek.com/167195/how-to-change-your-raspberry-pi-or-other-linux-devices-hostname/

[here]: http://sizious.com/2015/08/28/setting-a-static-ip-on-raspberry-pi-on-raspbian-20150505/

[pi_config/dhcpcd.conf]: pi_config/dhcpcd.conf

[pi_config/interfaces]: pi_config/interfaces

##### Cloning your Raspberry Pi: #####
  * After setting up the first Raspberry Pi, you will want to clone the image and copy it onto all your other Raspberry PI SD Cards.
      * Follow any of these guides to backup then restore (clone) your Raspberry PI Image.
          * [Cloning Your Raspberry PI (Windows)][]
          * [Clone Raspberry PI All Operating Systems][]
      * In general, backup the image then use that image to restore it onto all the other SD cards. You can use Win32DiskImager on Windows or the `dd` tool in Linux.
  * After restoring/cloning the image onto each SD card, make sure to change its hostname to be unique. You can do this two ways with either a Linux or Apple machine or a Raspberry Pi connected to monitor and keyboard:
      * Navigate to the folder where the SD card is mounted, `/media` for Linux and `/Volumes` for Apple.
          * Follow the instructions in the hostname section above.
          * Ignore the section with `sudo /etc/init.d/hostname.sh` since the sd card isn't booted up into the operating system at the moment and when it gets put into a rPI and is powered on is essentially the same.
      * Put the SD card into a rPI connected to a monitor, keyboard, and mouse and follow the hostname change section above.
  * *The hostname change section has to be done for each and every SD card that will be placed in a different Raspberry Pi!*

[this documentation.]: https://www.raspberrypi.org/documentation/linux/filesystem/backup.md

[Cloning Your Raspberry PI (Windows)]: http://lifehacker.com/how-to-clone-your-raspberry-pi-sd-card-for-super-easy-r-1261113524

[Clone Raspberry PI All Operating Systems]: http://www.htpcguides.com/easy-resize-and-back-up-raspberry-pi-sd-card-with-ubuntu/

[Follow these instructions for enabling and installing the camera.]: https://www.raspberrypi.org/documentation/usage/camera/README.md
  
### Using Ansible To Manage The Bramble ###

#### General Ansible Configuration Files ####

  * You can now start to manage your Bramble with Ansible on the centralized server.
  * Lets start by making a hosts file also known as the [Ansible Inventory][].
      * A sample hosts file from our configuration is here: [hosts](hosts).
          * All our rPIs are referred to by their IP address, but they don't need to be if your network identifies them by hostname.
          * If you could previously connect via ssh by hostname, you don't need ip addresses. You could also `ping <HostnameOfRaspberryPi>` to test.
      * Use it as a guide, but almost everything in the hosts file must be different and specific to your setup.
      * I find it useful to define a group with localhost (the server) for use in playbooks. In our hosts file, it is the `clizarraga_chronos` group.
  * If you need to use proxy settings or specific ssh settings, then you need to edit the [ansible configuration file][].
      * A sample configuration file is here: [config](playbooks/ansible.cfg)
      * [Default configuration file from Ansible.][]
      * Most of the changes are for ssh options because of connectivity and interference issues. Head to the [playbooks folder readme][] for more information.

[Ansible Inventory]: http://docs.ansible.com/ansible/intro_inventory.html

[playbooks folder readme]: playbooks/README.md
  
[ansible configuration file]: http://docs.ansible.com/ansible/intro_configuration.html

[Default configuration file from Ansible.]: https://raw.githubusercontent.com/ansible/ansible/devel/examples/ansible.cfg

#### Ansible Playbooks ####
  * So, you've setup your Raspberry PIs and you have installed and set up Ansible with your own hosts and configuration file.
      * You should test your ansible install by running `ansible -m ping all` from a terminal on the Ansible server.
  * This repository contains a [playbooks folder][] with playbooks made to manage the Raspberry Pis via the centralized server.
      * Before changing any playbooks, please read the [ansible playbooks documentation][].
  * The playbooks have a lot of assumptions built into them:
      * All images taken on the rPI use [camera_single.py][].
      * All images on the rPI are stored in `/home/pi/Images/`
  * **Playbooks**
      * For all playbooks:
          * `gather_facts` doesn't need to be false if you don't have connectivity issues.
          * `when:` determines when a task will run if the variable after it is false, it will not run.
          * `become:` determines if the task will be run as a superuser.
          * `hosts: ` needs to be changed to your appropriate inventory group.
      * [copy-pictures.yml][] -- Needs to change to be specific to the user setup.
          * Variables `img_dir` and `local_dir` need to be changed.
              * `img_dir` needs to be changed only if you're not using `/home/pi/Images` on the rPIs as your image destination.
              * `local_dir` needs to be changed to where the image files will be stored on the centralized server.
      * [sudo-plays.yml][] -- Contains true/false variables that need to be changed depending on context.
          * The tasks containing `utmp`, `sshd`, or `DNS` are for connectivity issues.
              * In general, its best to leave them false.
          * Timezone task(s):
              * Change the `timezone_change` variable and change the `timezone` variable itself to your desired timezone.
              * Use one of the strings from the TZ column in this [list of TZ database timezones][]
          * Task: `Add hourly cron job from 5 AM to 9 PM`
              * Currently it takes images every hour between 5 AM (5) and 9 PM (21).
              * To understand more about cron, read `man cron` and the [Ansible cron module][].
          * Task: `Send camera_single.py to the rPIs`
              * Change `src:` to the absolute path of `camera_single.py` on your Ansible server.
          * There is a secondary playbook in the file aimed at the localhost (`clizarraga_chronos`) to set up a cron job on it.
              * Change the `hosts:` to your localhost designation in your hosts/inventory file.
              * Change the `jobs="cd <YourPlaybooksDirectoryHere> && time bash -x playbook-ansible.sh -i <YourHostsFileHere> -vv`
                  * The `-f 2` option forces Ansible to do only two at a time instead of its usual 5. You can also set it to more processes at once if you want.
      * [wireless-power.yml][] -- Sends the [interfaces][] file to the rPIs.
          * Change the `src:` to the absolute path of the `interfaces` file on your Ansible server.
      * [take-pictures.yml][] -- Sends command to the hosts to call `camera_single.py`.
  * **Playbook-Ansible Bash Script**
      * The [playbook-ansible.sh][] script needs two major things:
          * If Ansible is installed via the package manager
              * Comment out line 2 of the script
                  * `source /home/clizarraga/usr/local/ansible/hacking/env-setup`
              * Uncomment line 3 of the script
                  * `# ansible-playbook=/usr/bin/ansible-playbook`
          * Otherwise, if you used the github installation mechanism:
              * Replace `/home/clizarraga/usr/local/ansible/hacking/env-setup` with the `<path/to/ansible>/hacking/env-setup`
          * The script uses a `logs` directory to store logs named by playbook and `year-month-date`. Make sure there is a logs directory in the path that the script is in. You can make one by running `mkdir logs` in the path to the bash script.
              
[playbooks folder]: playbooks/

[ansible playbooks documentation]: http://docs.ansible.com/ansible/playbooks_intro.html

[camera_single.py]: pi_files/camera_single.py

[copy-pictures.yml]: playbooks/copy-pictures.yml

[sudo-plays.yml]: playbooks/sudo-plays.yml

[Ansible cron module]: http://docs.ansible.com/ansible/cron_module.html

[wireless-power.yml]: playbooks/wireless-power.yml

[interfaces]: pi_files/interfaces

[take-pictures.yml]: playbooks/take-pictures.yml

[playbook-ansible.sh]: playbooks/playbook-ansible.sh

[list of TZ database timezones]: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones

### Final Notes ###
  * You can manage the bramble via Ansible with more playbooks that you can create yourself using the documentation provided above. You can also use the playbooks as a template for future playbooks.
  * A good way to test some Ansible commands beforehand is to use Ansible modules with [ad-hoc commands][]
      * `ansible -m ping all` or `ansible -m command -a ls` are good examples.

[ad-hoc commands]: http://docs.ansible.com/ansible/intro_adhoc.html
