#!/bin/bash
#Executed at system start up
#Modify ~/.config/lxsession/LXDE-pi/autostart to run this script
#Could start this bash script using any other method too but it is imperative that it is executed AFTER LX Desktop Environment has fully loaded and that it is run as the user logging in
lxterminal -e "bash -i /home/pi/aerial/bashbash.sh" &
