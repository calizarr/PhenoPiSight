end=$1
cidr=$2
ap=$3
ip=$4
bash -ex change_config.sh "$end" "$cidr" "$ap" "$ip"

cat dhcpcd.conf
cat hosts
cat hostname
echo "Checking SSID"
cat wpa_supplicant.conf

read -n 1 -s

etc=$5
mnt=$6
sudo bash -x copy_config.sh $etc $mnt
