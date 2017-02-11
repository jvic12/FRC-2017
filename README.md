# FRC-2017 Notes


## Required repos

The following [athenian-robotics github repos](https://github.com/athenian-robotics) should be cloned to *~pi/git*:

* [common-robotics](https://github.com/athenian-robotics/common-robotics): `git clone https://github.com/athenian-robotics/common-robotics.git`
* [object-tracking](https://github.com/athenian-robotics/object-tracking): `git clone https://github.com/athenian-robotics/object-tracking.git`
* [FRC-2017](https://github.com/athenian-robotics/FRC-2017): `git clone https://github.com/athenian-robotics/FRC-2017.git`

## Launching scripts

* Shell scripts are found in *~pi/git/FRC-2017/bin*. All changes to these scripts
should be pushed to github and not done as a one-off edit on the Raspi. The goal 
is provision a Raspi with `git` and minimize the amount of configuration 
on the Raspi. 

* Shell script stdout and stderr are redirected to *~pi/git/FRC-2017/logs*.

* Shell scripts are launched from */etc/rc.local* during startup.
The shell script calls are added just before the call to `exit 0` and are executed as user *pi*:
````bash
su - pi -c ~pi/git/FRC-2017/bin/object-tracker.sh
su - pi -c ~pi/git/FRC-2017/bin/gear-front-publisher.sh

exit 0
````

* Shell scripts running Python code using OpenCV need to first setup a *cv2* environment:
```bash
source ~pi/.profile
workon py2cv3
```

* *$PYTHONPATH* must be set appropriately to include dependent packages:
```bash
export PYTHONPATH=${PYTHONPATH}:~pi/git/common-robotics:~pi/git/object-tracking
```

* The *stdout* and *stderr* are included in the log file by using `&>`. It is critical that each shell script
be forked with a trailing `&`:
```bash
python2 ~pi/git/object-tracking/object_tracker.py --bgr "174, 56, 5" --width 400 --flip &> ~pi/git/FRC-2017/logs/object-tracker.out &
```

## Setting up remote repos on a Raspi

### FRC-2017 Repo

Setup a bare repo and a source directory:

```bash
cd git

mkdir FRC-2017
mkdir FRC-2017.git
git init --bare FRC-2017.git
```

Edit *FRC-2017.git/hooks/post-receive* and put this into it: 

```bash
#!/bin/sh
git --work-tree=/home/pi/git/FRC-2017 --git-dir=/home/pi/git/FRC-2017.git checkout -f
echo "*** Updated FRC-2017 ***" >&2
```

Make *post-receive* executable:
```bash
chmod +x FRC-2017.git/hooks/post-receive
```
Adjust the git config on your Mac (change raspiXX to your raspi hostname):

```bash
cd FRC-2017
git remote add raspiXX pi@raspiXX.local:/home/pi/git/FRC-2017.git
```

Push to the Raspi:
```bash
git push raspiXX master
```

### common-robotics Repo

Setup a bare repo and a source directory:

```bash
cd git

mkdir common-robotics
mkdir common-robotics.git
git init --bare common-robotics.git
```

Edit *common-robotics.git/hooks/post-receive* and put this into it: 

```bash
#!/bin/sh
git --work-tree=/home/pi/git/common-robotics --git-dir=/home/pi/git/common-robotics.git checkout -f
echo "*** Updated common-robotics.git ***" >&2
```

Make *post-receive* executable:
```bash
chmod +x common-robotics.git/hooks/post-receive
```

Adjust the git config on your Mac (change raspiXX to your raspi hostname):

```bash
cd common-robotics
git remote add raspiXX pi@raspiXX.local:/home/pi/git/common-robotics.git
```

Push to the Raspi:
```bash
cd common-robotics
git push raspiXX master
```

### object-tracking Repo

Setup a bare repo and a source directory:

```bash
cd git

mkdir object-tracking
mkdir object-tracking.git
git init --bare object-tracking.git
```

Edit *object-tracking.git/hooks/post-receive* and put this into it: 

```bash
#!/bin/sh
git --work-tree=/home/pi/git/object-tracking --git-dir=/home/pi/git/object-tracking.git checkout -f
echo "*** Updated object-tracking.git ***" >&2
```

Make *post-receive* executable:
```bash
chmod +x object-tracking.git/hooks/post-receive
```

Adjust the git config on your Mac (change raspiXX to your raspi hostname):

```bash
cd object-tracking
git remote add raspiXX pi@raspiXX.local:/home/pi/git/object-tracking.git
```

Push to the Raspi:
```bash
cd object-tracking
git push raspiXX master
```

## Topic names 
* "camera/gear/x" - topic for camera center position and screen width (int, int)
* "camera/gear/alignment" - topic for camera relative to object and command (int, String)
* "lidar/left" - topic for left lidar distance (int) 
* "lidar/right" - topic for right lidar distance (int)
* "lidar/distance" - topic for distance and command (int, int, String)
* "mqtt-turtle.local" - mqtt hostname

## Raspi Names
* 10 = lidar-gear-right - repos: common-robotics, FRC-2017 
* 11 = camera-gear - repos: common-robotics, FRC-2017, object-tracker
* 12 = mqtt-turtle - repos: none
* 21 = lidar-gear-left - repos: common-robotics, FRC-2017