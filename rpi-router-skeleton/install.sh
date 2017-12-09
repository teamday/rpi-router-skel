sudo dpkg --set-selections < packages.list
sudo apt-get -y update
sudo apt-get dselect-upgrade
