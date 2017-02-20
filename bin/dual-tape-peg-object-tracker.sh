#!/usr/bin/env bash
source ~pi/.profile
workon py2cv3
date > ~pi/git/FRC-2017/logs/dualtape-peg-object-tracker.reboot
sleep 5
export PYTHONPATH=${PYTHONPATH}:~pi/git/common-robotics:~pi/git/object-tracking
python2 ~pi/git/object-tracking/multi_object_tracker.py --dualbgr "188, 86, 254" --singlebgr "174, 56, 5" --width 400 --delay 0.25 --flipy --usb --http "camera-gear.local:8080" &> ~pi/git/FRC-2017/logs/dualtape-peg-object-tracker.out &


# 174, 56, 5 is blue
# 46, 43, 144 is red box