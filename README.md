# thecage
The Cage is an autonomous aerial drone charger, primarily designed for Parrot Bebop but meant to be utilized with ease for any other model. This repository is the code base that is run on The Cage.

## Features
- Different modes of operation
    - Autonomous operation via Robot Operating System (ROS) over Wi-Fi
    - Remote operation via Robot Operating System (ROS) or Pyrasite
    - Manual operation via Touchscreen GUI in person
- Fully multi-threaded
- Balance charges up to 3 cell batteries of LiPo, Li-Ion, LiFe, NiMH, NiCd & Pb types
- Conductive wireless charging

## System Requirements
- 900Mhz Processor
- 1GB RAM
- 4 Analog, 1 Set of I2C, 8 GPIO, 8 PWM pins (or 8 more GPIO but with software PWM)
- Touchscreen (Optional)
- 1S-3S Battery Charger with USB interface
    - Hyperion EOS 0720i NET3-AD is used in our setup
    - Can use any other commercial charger, just need to replace the instruction set in the battery.py file with new serial commands
- Raspbian, Ubuntu or Debian
- Python 2.7
- [PySide](https://pypi.python.org/pypi/PySide/1.2.4) (Dynamically linked)
- [Adafruit ADS1x15 Library](https://learn.adafruit.com/raspberry-pi-analog-to-digital-converters/ads1015-slash-ads1115) (..or another ADC library that fits your hardware)
- [ROS Indigo](http://wiki.ros.org/indigo)

## Installation
1) Install ROS Indigo

2) Copy thecage files to ~/aerial

3) Modify autostart to execute runme.sh

    - Autostart is at ~/.config/lxsession/LXDE-pi/autostart for Raspbian following on Raspberry Pi 2
    
    - Read runme.sh for more details

4) Make sure all files in ~/aerial have at least READ and EXECUTE permissions for the user used for logging in

    - A good and secure permission would be 750 with CHMOD
    
## Credits
Mehmet Akbulut developed most of the electronics and software.

Zoe Dickert wrote a good chunk of battery.py and sandwich.py along with assisting with electronics and mechanical design.

Benjamin Ha, Samuel Black and Kamiko Darrow worked tirelessly to get the mechanical setup ready.

Boston University Robotics Lab was the first client that made this entire project possible.

## License
MIT License
In short: you can reuse it for any purpose without specifically asking for permission. All we ask is that credit be given where due. Please refer to LICENSE file if unsure.

**Thank you!**

[//]: # (...)

   [node.js]: <http://nodejs.org>
   [Twitter Bootstrap]: <http://twitter.github.com/bootstrap/>
   [keymaster.js]: <https://github.com/madrobby/keymaster>
   [jQuery]: <http://jquery.com>
   [express]: <http://expressjs.com>
   [AngularJS]: <http://angularjs.org>
   [Gulp]: <http://gulpjs.com>
