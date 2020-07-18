#!/bin/sh

apt install python3-systemd
mkdir /usr/lib/ds4autopair
cp ./ds4autopair.service /etc/systemd/system/
cp ./ds4autopair.py /usr/lib/ds4autopair/
cp ./bluetoothctl.py /usr/lib/ds4autopair/
chown root:root /etc/systemd/system/ds4autopair.service
chmod 755 /etc/systemd/system/ds4autopair.service
systemctl enable ds4autopair
