#!/bin/bash

# Push common-robotics repo
cd ~/git/common-robotics
git push camera-gear master
git push lidar-gear-left master
git push lidar-gear-right master

# Push FRC-2017 repo
cd ~/git/FRC-2017
git push camera-gear master
git push lidar-gear-left master
git push lidar-gear-right master

# Push object-tracking repo
cd ~/git/object-tracking
git push camera-gear master

# Reboot machines
ssh pi@camera-gear.local sudo reboot now
ssh pi@lidar-gear-left.local sudo reboot now
ssh pi@lidar-gear-right.local sudo reboot now
ssh pi@mqtt-turtle.local sudo reboot now
