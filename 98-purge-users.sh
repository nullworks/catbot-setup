#!/bin/bash

#
#	Will delete all catbot- users and their home directories
#

if [ $EUID == 0 ]; then
	echo "This script must not be run as root"
	exit
fi
echo "Doing this will delete all catbot users and folders."
read -p "Are you sure?"
for n in $(ls -1 /home | grep cat | wc -l)
do
	for u in $(seq 1 $n)
	do
		echo "Deleting user catbot-$u"
		sudo userdel -r catbot-$u
		sudo groupdel catbot-$u
		done
done

for p in $(ls -1 /home | grep catbot-)
do
	echo "Removing leftover folder $p"
	sudo rm -rf /home/$p
done
