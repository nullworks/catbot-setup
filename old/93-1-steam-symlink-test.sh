#!/bin/bash

if [ "$#" == 1 ]; then
	max=$1
fi
for i in $(seq 1 "$max")
do
sudo mkdir -p /home/"$(cat kisak)"-"$i"
sudo chown "$(cat kisak)"-"$i":"$(cat kisak)"s /home/"$(cat kisak)"-"$i"

sudo -H -u "$(cat kisak)"-"$i" bash -c "mkdir -p /home/$(cat kisak)-$i/.steam/steam"
sudo -H -u "$(cat kisak)"-"$i" bash -c "ln -s \"/opt/steamapps\" \"/home/$(cat kisak)-$i/.steam/steam/\""
sudo -H -u "$(cat kisak)"-"$i" bash -c "touch ~/.steam/steam_install_agreement.txt"
done
