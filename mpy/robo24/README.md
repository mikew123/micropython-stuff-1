Mike Williamson robot for 2024 DPRG ROBO-COLUMBUS

Forked Jon Hylands Universal Robot Controler and adding mods for my robot
    https://github.com/JonHylands/micropython-stuff.git

The Python code is copied to the ESP32 board using rshell
The code is copied using rshell->rsync . /pyboard (cd to dir with code or links)

Added urc-jon_links has links to Jon's controller for rshell->rsync
Added my own robo24 python code based on Jon's and added a robo20_links folder

The robo24 version of the urc_peer is in the Arduino repo because I needed to 
write it in C for my ESP32C6 board using its UART-USB connector to Pi ROS2

