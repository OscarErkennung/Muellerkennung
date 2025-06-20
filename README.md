# Oscar
Revolutionizing the Recycling System since 2025

# Installation
## Prerequisites: 
this assumes you have a Raspberry Pi 4B already setup and running, SSH enabled under ``raspi-config``.
### clone this repo: 
in your user directory, run ``git clone https://github.com/OscarErkennung/Muellerkennung``

#### venv: 
* initialize virtual environment: ``$ python -m venv .venv ``  
* activate virtual environment: 
``$ source .venv/bin/activate``

#### installing required packages: 
* install system packages:  
  * TBD
  * recommended python version is 3.11
* install python packages: 
  * make sure the venv is running, see above   
  * ``$ pip install -r requirements.txt``
# Usage
## access over ssh - applicable only for Gymnasium Höchstadt
The raspberry pi should be placed in a network where device can "see" each other, so *not* GH-Schüler! 
for finding out which specific IP Adress the router assigned to the Raspberry pi, run a generic Network scanner tool on your phone/laptop on the same network and look for the Network device with the name "Prusa i3Mk3s"[or similar].
### open connection
* execute ``$ ssh oscar@<your ip here>``   
* confirm the connection by entering a  password, and if applicable confirming the new unknown ssh key. 
### starting the webserver
* change from the home directory of oscar to the folder "Muellerkennung" by doing ``cd Muellerkennung``
* start the django webserver by executing ``python manage.py runserver 0.0.0.0:8000``

### You're done
* the webserver/control interface should now be available via any web browser via ``http://<your ip here>:8000/``   
* here you can access simple movement functions, see the status of the sensors and computer vision as well as start autonomous missions.

# etc
* you can cancel the django webserver by pressing "CTRL+C" in the command line where you executed it from. 
* a launch.json for debugging inside of VS code is provided. 
* for the current models, see training repo. copy these to the root directory and change the MODEL_PATH accordingly. 
* 

## 🍪🍪 MMMMMMMMM COOOOKIE🍪🍪

