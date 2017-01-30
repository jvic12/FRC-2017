#! /bin/bash

echo "Gear front publisher..."
export PYTHONPATH=${PYTHONPATH}:~pi/git/common-robotics:~pi/git/object-tracking
~pi/git/FRC-2017/location_publisher.py --grpc raspi11.local --camera camera-gear-front --mqtt mqtt-turtle.local

