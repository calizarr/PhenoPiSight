Installation, setup, and user guide
===================================

### Getting Started ###
  * Raspberry Pis will require some usage of the Linux terminal and its worth knowing how to get around a bit. The Raspberry Pi foundation provides a [quick tutorial][].
  * As great as it is, it does not give you information on how to use `nano` the default Linux text editor:
      * [Beginnner's Guide to Nano][]
      * [Nano Basics][]
  * Many of the Raspberry Pi camera commands can be better used with the Python library included with Raspbian. The Raspberry Pi foundation also provides a [quick python tutorial][].
  * Feel free to refer back to these links as you go through the installation steps for the Raspberry Pi as well as Ansible.

[quick tutorial]: https://www.raspberrypi.org/documentation/usage/terminal/README.md

[Beginnner's Guide to Nano]: http://www.howtogeek.com/howto/42980/the-beginners-guide-to-nano-the-linux-command-line-text-editor/

[Nano Basics]: https://wiki.gentoo.org/wiki/Nano/Basics_Guide

[quick python tutorial]: https://www.raspberrypi.org/documentation/usage/python/README.md


### Raspberry Pi Setup ###
  * [Raspberry PI Quick Start Guide][]
  * First configure the Raspberry Pi which will be used to make the image to clone onto all the other Raspberry PIs.
  * **Follow this documentation:** [Raspberry Pi Installing Operating Systems][]
  * [Debian jessie][] is the recommmended raspbian distribution.
  * ***To avoid problems in the future, make sure that your SD card used for cloning is the smallest SD card you have. Even if they claim to be of the same size -- 8 GBs is not the same across all SD cards.***
      * Linux Terminal: Open a terminal, type or copy/paste `df -h`, and look at the  `/dev/root` Filesystem and its `Size` parameter.
      * Windows: Go into Windows Explorer, Right click the SD card and check the capacity.
  * Follow all the prompts after installing Raspbian/Debian Jessie onto the Original Raspberry Pi, then continue onward.

##### * Setting up your Raspberry Pi: #####

      * Log in to the Original Raspberry PI using a usb mouse and keyboard and an HDMI capable monitor.
      * WiFi:
          * Set up the network following instructions for GUI: [GUI WiFi Setup][]
          * If using the command line follow this set of instructions: [Raspberry PI CLI setup][]
      * Camera:
          * [Follow these instructions for enabling and installing the camera.][]
      * Hostname:
          * [Change hostname using command line][]
          * Make sure to give your Raspberry PI a unique hostname.
              * Ours go from ShakoorCamera11 to ShakoorCamera190 so that they do not conflict.
              * We also gave ours static IP addresses from 10.9.0.11 to 10.9.0.190.
              * Given the density of our bramble we had to provide static IP addresses, but it may not be necessary otherwise.
              * Static IP Addresses are a bit more complicated but they are documented [here][].
                  * The previous GUI WiFi Setup also includes some information on static IP addresses.
              * Also take a look at the file in [pi_config/dhcpcd.conf][] for an idea of what to put in your dhcpcd.conf
                  * Your `domain_name_servers`, `ip_address`, `routers`, and `hostname` will be different
      * Wireless Transmit Power:
          * Go to a terminal and type:
              * `sudo nano /etc/network/interfaces` under wlan0 type: `wireless-power off`
              * exit and save the file using Ctrl+X and agreeing to all prompts.
              * This removes all wireless power management which prevents random disconnects.
          * If you want to change it to a lower transmit power to avoid WiFi interferences, use the `interfaces` file in [pi_config/interfaces][].
          * This is generally unnecessary, but if you experience communication issues having a lower transmit power may be useful.
          * The ansible playbook `wireless-power.yml` will copy the file over if you need to change it after all the rPIs are set up.
              * Look at [playbooks folder](playbooks) for more information.
  * Cloning your Raspberry Pi:
      * After setting up the first Raspberry Pi, you will want to clone the image and copy it onto all your other Raspberry PI SD Cards.
      * Follow any of these guides to backup then restore (clone) your Raspberry PI Image.
          * [Cloning Your Raspberry PI (Windows)][]
          * [Clone Raspberry PI All Operating Systems][]
          * In general, backup the image then use that image to restore it onto all the other SD cards. You can use Win32DiskImager on Windows or the `dd` tool in Linux.
      * After restoring/cloning each image onto an SD card, make sure to change its hostname to be unique. You can do this two ways on either a Linux or Apple machine:
          * Navigate to the folder where the SD card is mounted, `/media` for Linux and `/Volumes` for Apple.
              * Follow the instructions in the hostname section above.
              * Ignore the section with `sudo /etc/init.d/hostname.sh` since the sd card isn't booted up into the operating system at the moment and when it gets put into a rPI and is powered on is essentially the same.
          * Put the SD card into a rPI connected to a monitor, keyboard, and mouse and follow the hostname change section above.

[this documentation.]: https://www.raspberrypi.org/documentation/linux/filesystem/backup.md

[Cloning Your Raspberry PI (Windows)]: http://lifehacker.com/how-to-clone-your-raspberry-pi-sd-card-for-super-easy-r-1261113524

[Clone Raspberry PI All Operating Systems]: http://www.htpcguides.com/easy-resize-and-back-up-raspberry-pi-sd-card-with-ubuntu/

[Follow these instructions for enabling and installing the camera.]: https://www.raspberrypi.org/documentation/usage/camera/README.md

### Ansible Setup ###
  * Depending on the setup of the centralized server that will be launching Ansible, you will need to pick what is best for you from the [Ansible installation documentation][].
  * I have installed ansible from source using github for a rootless installation.
  * Ansible setup is rather straightforward and should not be very problematic.
  
### Using Ansible To Manage The Bramble ###
  * So, you've setup your Raspberry PIs and you have installed Ansible, now you need to clone this github repository if you haven't already.
  * First, a GitHub primer to get you started: [GitHub Introduction: Hello World!][]
  * Then, once you are finished with that type:
  * `git clone git@github.com:calizarr/EPSCOR_Bramble_GH9C.git` to clone this repository into a folder named EPSCOR\_Bramble\_GH9C.
  * The files you'll need from this repository aren't many.
      * All of the playbooks (yml files) assume that the rPI image directory is `/home/pi/Images/`.
      * [hosts](hosts) -- [Ansible Inventory][] and needs to be configured for your setup.
          * I find it useful to declare the localhost as its own group in the inventory file. In this case, it is `clizarraga_chronos` and some of the playbooks use it later. You can change it to your preference or keep using my name for it although I suggest changing it.
      * ansible.cfg -- should be completely configured for your own setup.
          * Use it as a guide, but don't copy directly. Generally just stick to ansible defaults unless you need to change them.
      * Playbooks:
          * Before changing any playbooks, please read the [ansible playbooks documentation][].
          * All of the playbooks will need their hosts variable changed, please do so before attempting to run any of them.
          * copy-pictures.yml -- needs some changes to be useful to your setup.
              * `img_dir` and `local_dir` need to be changed.
                  * `img_dir` needs to be changed only if you're not using `/home/pi/Images` on the rPIs as your image destination.
                  * `local_dir` needs to be changed to where the image files will be stored not on the rPIs.
          * sudo-plays.yml -- contains true/false variables that need to be changed depending on context.
              * You might need to change the `Add hourly cron job from 5 AM to 9 PM` task.
                  * To understand more about cron, read `man cron` and the [Ansible cron module][].
              * Change the `src:` variable on the `Send camera_single.py to the rPIs` task to the destination of camera_single.py of this repository.

[Raspberry Pi Installing Operating Systems]: https://www.raspberrypi.org/documentation/installation/installing-images/

[debian jessie]: https://www.raspberrypi.org/downloads/raspbian/

[Raspberry PI CLI setup]: https://www.raspberrypi.org/documentation/configuration/wireless/wireless-cli.md

[Raspberry PI Quick Start Guide]: https://www.raspberrypi.org/help/quick-start-guide/

[GUI WiFi Setup]: https://www.raspberrypi.org/blog/another-raspbian-desktop-user-interface-update/

[Change hostname using command line]: http://www.howtogeek.com/167195/how-to-change-your-raspberry-pi-or-other-linux-devices-hostname/

[here]: http://sizious.com/2015/08/28/setting-a-static-ip-on-raspberry-pi-on-raspbian-20150505/

[pi_config/dhcpcd.conf]: pi_config/dhcpcd.conf

[pi_config/interfaces]: pi_config/interfaces

[Ansible installation documentation]: http://docs.ansible.com/ansible/intro_installation.html

[GitHub Introduction: Hello World!]: https://guides.github.com/activities/hello-world/

[Ansible Inventory]: http://docs.ansible.com/ansible/intro_inventory.html

[ansible playbooks documentation]: http://docs.ansible.com/ansible/playbooks_intro.html

[Ansible cron module]: http://docs.ansible.com/ansible/cron_module.html

