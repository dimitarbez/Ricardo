# Ricardo

![Image of Yaktocat](https://github.com/dimitarbez/Ricardo/blob/master/ricardo.jpg)

### 1. Introduction
  Ricardo is an open-source robot which aim is to make replicating it an easy and fun process
  so that anyone who is interested in robotics can get into the field and progress.
  Ricardo is fully 3D printable and uses some 3D models from thingiverse. The electronics are
  all readily available and relatively cheap such as the Raspberry Pi and other Arduino modules
  which make upgrading and repairing him an easy process.
  This document contains a guide in the following sections on all of the parts and how they are
  connected so that you can easily start making your own Ricardo.
  The README file shall be updated consistently with new changes and it is the documentation 
  for the entire project.
    
### 2. Project structure
  #### 1. Files 
  The repository consists of several python scripts which will need to be runned from the
  Raspberry Pi for all of this to work. You need this repository cloned on your Raspberry Pi.
  The scripts can be divided into two categories: **user driven** and **AI driven**.
  In the user driven scripts (ex: robot_control.py) the user inputs commands in order to
  control the robot. In the AI driven scripts the AI controls the robot either entirely or lets
  the user also have some control.
  
  #### 2. Physical architecture
  Ricardo's "_brain_" is a Raspberry Pi. It controls all of the parts. The Raspberry Pi either 
  connects to a WiFi router or it just becomes a hotspot and devices can connect to it in order
  to envoke the scripts via ssh or vnc. The robot has four motors that drive the two tank tracks. 
  These motors are driven by the L298N motor driver which gets inputs from the Raspberry Pi directly.
  For vision the robot uses the Pi Camera module mounted on a camera rotating system driven by
  two servo motors.
  The robot also has accessories such as front lights and a horn (more accessories can be added)
  The Raspberry Pi and the accessories (including camera rotation servos) are powered on a 
  20000 mAh power bank. Everything on the robot is powered with the 5V power bank except the L298N
  motor controller which uses 2x18650 batteries in serial (7.4V) which works well for the motors.

### 3. Functionalities and logic
  #### 1. AI driven
  * Robot follows person by tracking their face (face_tracker_picam.py)
    * If tracked face enters left region the robot turns left
    * If tracked face enters right region the robot turns right
    * If the tracked face enters the left and right turning trigger
      area then it continues operating normally and does not rotate
    * Moving forward and backward are done by calculating the 
      area of the tracked face. If the face area is larger than
      a ceratin threshold, then the robot drives backwards from
      the person. if the face area is smaller than a certain
      threshold, then the robot drives towards the user
    
  #### 2. User driven
  * Remote control of the robot (robot_control.py)
    * Live video preview
    * Ability to capture video
    * Ability to take pictures
    * Manual camera rotation
    * Manual motor control
    * Ability to use front LED lights
    * Ability to use horn
    
### 4. Parts
  #### 1. Electronic connections with Raspberry Pi GPIO pins
  Component | GPIO Board pin
  ----------|---------------
  Buzzer | 37
  Front LED lights | 36
  Motor 2 PWM | 10
  Motor 1 PWM | 8
  Motor IN1 | 5
  Motor IN2 | 11
  Motor IN3 | 13
  Motor IN4 | 15
  Camera yaw servo | 40
  Camera pitch servo | 38
  Antenna (rpitx) | 7
  
  
  
    
