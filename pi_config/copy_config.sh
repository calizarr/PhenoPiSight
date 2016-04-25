#!/bin/bash
# $1 is the etc/ of the SD card (/media/calizarr/44.../etc/)
# $2 is the mount point of the SD card (/dev/sdd[123]+)
cp dhcpcd.conf $1
cp hosts $1
cp hostname $1
cp wpa_supplicant.conf $1/wpa_supplicant/
cp interfaces $1/network/interfaces
rm $1/ssh/ssh_host_*

sudo /usr/bin/ssh-keygen -t rsa1 -f $1/ssh/ssh_host_key -N ''
sudo /usr/bin/ssh-keygen -t rsa -f $1/ssh/ssh_host_rsa_key -N ''
sudo /usr/bin/ssh-keygen -t dsa -f $1/ssh/ssh_host_dsa_key -N ''
sudo /usr/bin/ssh-keygen -t ecdsa -f $1/ssh/ssh_host_ecdsa_key -N ''
sudo /usr/bin/ssh-keygen -t ed25519 -f $1/ssh/ssh_host_ed25519_key -N ''

# Unmounting card
sudo umount $21
sudo umount $22
