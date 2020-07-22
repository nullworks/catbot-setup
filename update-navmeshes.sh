#!/usr/bin/env bash

# Fetches and updates navmeshes



echo "Fetching navmeshes..."
git clone --depth 1 https://github.com/nullworks/catbot-database
clone_status=$?

if [ $clone_status -eq 128 ]; then
	pushd catbot-database
	if [ $? -eq 0 ]; then
		echo -e "\nRepository exists, trying to pull from upstream..."
		git pull
		if [ $? -ne 0 ]; then # Unclean working tree?
			echo -e "\nError pulling from upstream; exiting."
			exit 1
		fi
		popd
	else # Network trouble?
		echo -e "\nError cloning the repository; exiting."
		exit 1
	fi
fi


echo -e "\nCopying navmeshes..."
cp catbot-database/nav\ meshes/*.nav ~/.steam/steam/steamapps/common/Team\ Fortress\ 2/tf/maps/
chmod 644 -R ~/.steam/steam/steamapps/common/Team\ Fortress\ 2/tf/maps/*.nav


# Don't delete catbot-database if it existed prior to running this script
if [ $clone_status -eq 0 ]; then
	echo -e "\nCleaning up..."
	rm -rf catbot-database
fi


echo "Done."
