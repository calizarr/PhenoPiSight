Installation, setup, and user guide
===================================

### Raspberry Pi Setup ###
  * [Raspberry PI Quick Start Guide][]
  * To first configure the Raspberry Pi which will be used to make the image to clone onto all the other Raspberry PIs follow this documentation: [Raspberry Pi Installing Operating Systems][]
  * I used [debian jessie][] and would recommend it.
  * To avoid problems in the future, make sure that your SD card used for cloning is the smallest SD card you have. Even if they claim to be of the same size -- 8 GBs is not the same across all SD cards.
      * Linux Terminal: `df -h` check /dev/root and view look for the Size parameter.
      * Windows: Go into Windows Explorer, Right click the SD card and check the capacity.
  * Setting up your Raspberry Pi:
      * Log in to the Original Raspberry PI using a usb mouse and keyboard and an HDMI capable monitor.
      * WiFi:
          * Set up the network following instructions for GUI: [GUI WiFi Setup][]
          * If using the command line follow this set of instructions: [Raspberry PI CLI setup][]
      * Hostname:
          * [Change hostname using command line][]
          * Make sure to give your Raspberry PI a unique hostname.
              * Ours go from ShakoorCamera11 to ShakoorCamera190 so that they do not conflict.
              * We also gave ours static IP addresses from 10.9.0.11 to 10.9.0.190.
              * Given the density of our bramble we had to provide static IP addresses, but it may not be necessary otherwise.
              * Static IP Addresses are a bit more complicated but they are documented [here][].
              * Also take a look at the file in [pi_config/dhcpcd.conf][] for an idea of what to put in your dhcpcd.conf
                  * Your domain_name\_servers, ip_address, routers, and hostname will be different
              * 

[Raspberry Pi Installing Operating Systems]: https://www.raspberrypi.org/documentation/installation/installing-images/

[debian jessie]: https://www.raspberrypi.org/downloads/raspbian/

[Raspberry PI CLI setup]: https://www.raspberrypi.org/documentation/configuration/wireless/wireless-cli.md

[Raspberry PI Quick Start Guide]: https://www.raspberrypi.org/help/quick-start-guide/

[GUI WiFi Setup]: https://www.raspberrypi.org/blog/another-raspbian-desktop-user-interface-update/

[Change hostname using command line]: http://www.howtogeek.com/167195/how-to-change-your-raspberry-pi-or-other-linux-devices-hostname/

[here]: http://sizious.com/2015/08/28/setting-a-static-ip-on-raspberry-pi-on-raspbian-20150505/

[pi_config/dhcpcd.conf]: pi_config/dhcpcd.conf

