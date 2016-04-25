#!/bin/bash
# End should be passed in as a straight number end=245
end=$1
# CIDR should be passed in as "\/16"
cidr=$2
# ap should be passed in as a straight number
ap=$3
# IP capture (first 3 subnet mask digits with trailing period)
ip=$4

sed -ri "s/(static ip_address=$ip)(.*)/\1$end$cidr/" dhcpcd.conf
sed -ri "s/(hostname ShakoorCamera)(.*)/\1$end/" dhcpcd.conf

sed -ri "s/(ssid=\"Danforth_Shakoor)(.*)/\1$ap\"/" wpa_supplicant.conf
sed -ri "s/^($ip)[0-9]+(.*)/\1$end\2/" hosts
sed -ri "s/ShakoorCamera[0-9]+/ShakoorCamera$end/g" hosts
sed -ri "s/ShakoorCamera[0-9]+/ShakoorCamera$end/g" hostname

