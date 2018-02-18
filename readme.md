# Mutation GUI

This Gui is meant to be used within the setting of the Mutation project. 
Mutation is an audio-visual installation, conducted at the MUT building of 
the University of Music Karlsruhe, mainly by students of the third semester
in music informatics.
The technical setup may vary slightly each year. In 2018 five host computers
with eight projectors were used for the visuals. The host computers were
controlled by one main computer. The idea of this GUI was to ease and speed up
the controlling of the hosts and their projectors.

## Functionality
 The Gui's purpose mainly is to display information on the hosts and projectors.
 The information it needs to do so is taken from the configuration given in
 config.py. Hence in order to adopt the Gui for your Mutation project, you
 first need to adapt the settings in config.py.
 
 The different functions behind the buttons are mostly achieved via
 calling of bash commands or apple scripts from within python 
 using the subprocess library.
 Some commands are also send via osc to the BetterChecker3000 App or seperate
 SuperCollider scripts.
 

## Requirements

It is recommended to use Python 2.7, as the Gui was only tested with this 
python version. In any case you need to use Python 2.x because the library
used for osc communication only works with Python 2.x.
To install the library used for osc communication, do

`$ pip install pyOSC`

Furthermore, to enable host communication via ssh, ssh-keys must be generated
for all hosts. This was done using 
[this instruction](https://www.digitalocean.com/community/tutorials/how-to-set-up-ssh-keys--2).

To be able to update the files on all hosts prsync must be installed.

Note that you should have the BetterChecker3000 App v1, and if there 
is second projector also v2, on every host's Desktop. 
Moreover on the main computer on the path given in config.py as basepath
there should be all files which are needed by the groups on every host
to run the different visualisation apps.


## Usage

Download or clone this repository. Then from within the repository folder simply do

`$ python2 gui.py`.

For verbose logging output do

`$ python2 gui.py -v`.


## Future TODOs

### Update button
The update functionality could be improved in the future.
Up to now all files found in basepath of config.py are copied (using rsync or scp)
to all hosts. This process could be speed up if for every host, only the files
which are needed on this hosts are copied.
Furthermore parallel processing could be used.

### Restart and Shutdown buttons
Up to now the restart and shutdown buttons do not work.
The problem is, that both commands need to be run with sudo.
Two options were tested, both did not work, but could be tested in more detail:

1) `$ sudo chmod s+u /sbin/shutdown` and `$ sudo chmod s+u /sbin/reboot`
on every host seemed to work, but did not work the next day

2) Show password prompt with -t flag (see run_ssh_command() in bash.py)

Any other possibility to enable shutdown and restart without sudo could be tried as well. 
Maybe also apple scripting could be an idea.

### Quit button
Up to know apps are quit on every host by pressing 'cmd+q' several times 
(see method quit_any_apps() in hosts.py). 
This could be improved by making use of method quit_app() in projector.py.
Changes must be adopted to method quit_apps() in gui.py.

### Syphon and BetterChecker3000 App
Setting of the syphon server with the BetterChecker3000 App should be possible,
but somehow did not work yet. It could be not tested in more detail, 
because of the spontaneous transfer from the older CheckerApp to the
BetterChecker3000 App. It should be further tested.
 
### Individual group start / quit osc messages
In 2018 most groups had individual start and stop osc messages, in detail
implemented in a seperate SuperCollider file (see play_apps() and quit_apps()
in gui.py and compare with play_app() and quit_app() in projector.py). 
This could be improved by, e.g. deciding on equal framework usage and settings
for all groups or maybe also by improving the configuration settings in config.py.
maybe nicer config (especially start/stop with osc in seperate supercoolider script not so nice)

### Crop
Crop functionality of BetterChecker3000 App could not be tested yet.
Functionality for setting the crop values already exists in the Gui, but should
be tested and probably expanded in the future, e.g. implement a set_crop method
in projector.py, where the class attribute crop already exists (compare with osc 
message send from within load_video).
