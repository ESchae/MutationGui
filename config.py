basepath = '/Users/mutation/Desktop/Mutation2018Files/'
desktoppath = '/Users/mutation/Desktop/'

# all files that should be run from one of the hosts are stored in basepath
# within groups, each group specifies which app should be run on which
# projector, given the filename from within the group's folder in basepath
# e.g. if the content of basepath is
#
# basepath/TeamTest/
# basepath/TeamTest/play-me-on-projector_x.app
# basepath/TeamTest/play-me-on-projector-y.app
# basepath/MarninTobi/play_me_on_all_hosts.app
#
# TeamTest would specify 'play-me-on-host10-projector_x.app' as app for
# projector with name 'x' and 'play-me-on-projectory-y.app' as app for
# projector with name 'y'
#
# MarninTobi could specify 'play_me_on_all_hosts.app' as app for all
# projectors


# Note on syphon server app name:
# It is assumed that the app name is the same like the app name given
# in "app", e.g. for an app called /test/mycinder.app the cynder app name
# should be mycinder

groups = {
    'TeamTest': {
        'use_checker': True,
        'video': False,
        # for each projector, specify which app should be run
        'projector_settings': {
            'top': {
                'app': 'xy.app',
                'syphon_server': ''
            },
            'L': {
                'app': 'x.app',
                'syphon_server': ''
            },
            'right': {
                'app': 'xy.app',
                'syphon_server': ''
            },
            'regie': {
                'app': 'x.app',
                'syphon_server': ''
            },
            'ceiling': {
                'app': 'xy.app',
                'syphon_server': ''
            },
            'left-front': {
                'app': 'x.app',
                'syphon_server': ''
            },
            'stairs': {
                'app': 'xy.app',
                'syphon_server': ''
            },
            'right-front': {
                'app': 'x.app',
                'syphon_server': ''
            }
        }
    },
    'MarninTobi': {
        'use_checker': False,
        'video': False,
        # for each projector, specify which app should be run
        'projector_settings': {
            'top': {
                'app': 'Test02_v2.app',
                'syphon_server': ''
            },
            'L': {
                'app': 'Test02_v1.app',
                'syphon_server': ''
            },
            'right': {
                'app': 'Test02_v1.app',
                'syphon_server': ''
            },
            'regie': {
                'app': 'Test02_v1.app',
                'syphon_server': ''
            },
            'ceiling': {
                'app': 'Test02_v2.app',
                'syphon_server': ''
            },
            'left-front': {
                'app': 'Test02_v1.app',
                'syphon_server': ''
            },
            'stairs': {
                'app': 'Test02_v2.app',
                'syphon_server': ''
            },
            'right-front': {
                'app': 'Test02_v1.app',
                'syphon_server': ''
            }
        }
    },
    'Alessandro': {
        'use_checker': True,
        'video': False,
        # for each projector, specify which app should be run
        'projector_settings': {
            'top': {
                'app': '10/Screen1/CinderProject.app',
                'syphon_server': 'screen1'
            },
            'L': {
                'app': '10/Screen2/CinderProject.app',
                'syphon_server': 'screen2'
            },
            'right': {
                'app': '12/Screen1/CinderProject.app',
                'syphon_server': 'screen1'
            },
            'regie': {
                'app': '13/Screen1/CinderProject.app',
                'syphon_server': 'screen1'
            },
            'ceiling': {
                'app': '14/Screen1/CinderProject.app',
                'syphon_server': 'screen1'
            },
            'left-front': {
                'app': '14/Screen2/CinderProject.app',
                'syphon_server': 'screen2'
            },
            'stairs': {
                'app': '15/Screen1/CinderProject.app',
                'syphon_server': 'screen1'
            },
            'right-front': {
                'app': '15/Screen2/CinderProject.app',
                'syphon_server': 'screen2'
            }
        }
    },
    'Vanessa': {
        'use_checker': True,
        'video': True,
        # for each projector, specify which app should be run
        'projector_settings': {
            'top': {
                'app': '',
                'syphon_server': ''
            },
            'L': {
                'app': '',
                'syphon_server': ''
            },
            'right': {
                'app': 'Dancer_1.mp4',
                'syphon_server': ''
            },
            'regie': {
                'app': 'Dancer_2.mp4',
                'syphon_server': ''
            },
            'ceiling': {
                'app': '',
                'syphon_server': ''
            },
            'left-front': {
                'app': 'Dancer_3.mp4',
                'syphon_server': ''
            },
            'stairs': {
                'app': '',
                'syphon_server': ''
            },
            'right-front': {
                'app': 'Dancer_4.mp4',
                'syphon_server': ''
            }
        }
    },
    'Tim': {
        'use_checker': True,
        'video': False,
        # for each projector, specify which app should be run
        'projector_settings': {
            'top': {
                'app': 'Mutationfinished/example-BasicCopied.app',
                'syphon_server': ''
            },
            'L': {
                'app': 'Mutationfinished/example-BasicCopied.app',
                'syphon_server': ''
            },
            'right': {
                'app': 'Mutationfinished/example-BasicCopied.app',
                'syphon_server': ''
            },
            'regie': {
                'app': 'Mutationfinished/example-BasicCopied.app',
                'syphon_server': ''
            },
            'ceiling': {
                'app': 'Mutationfinished/example-BasicCopied.app',
                'syphon_server': ''
            },
            'left-front': {
                'app': 'Mutationfinished/example-BasicCopied.app',
                'syphon_server': ''
            },
            'stairs': {
                'app': 'Mutationfinished/example-BasicCopied.app',
                'syphon_server': ''
            },
            'right-front': {
                'app': 'Mutationfinished/example-BasicCopied.app',
                'syphon_server': ''
            }
        }
    }
}

# Projector name is as name to describe its shape or position and to easily
# find its 'real' place in MUT.

# Projector position is the monitor position of the projector if you open
# screen share of the host to which belongs the projector. Possible options
# are: left, right or main, if only one projector is used.
# Note, that 'right-screen' means, that the monitor must be set in system
# preferences as the right monitor!


# IMPORTANT NOTE 1: The name of the corresponding checker app for a specific
# projector will be derived as follows:
#
# checker_<name>_<position>/checker3.app !
#
# Hence you need to manually make sure that the right folder(s) lie(s) on the
# Desktop of every host.

# IMPORTANT NOTE 2: Right-screen must be listed before left-screen!
# This is because the apps will be opened one after one, on hosts with
# two projectors, first the app which should be run on right-screen will be
# opened automatically. This opens the app on the main monitor (left)
# and hence the app needs to be moved to the second (right) screen.
# This movement is done with an apple script called
# 'move_to_second_screen.scpt'* which must be on the Desktops of all hosts.
# After the app is moved to the second screen, full screen is toggled. Then
# the app which should run on the main (left) monitor is opened.

# * script taken from
# https://apple.stackexchange.com/questions/136324/moving-finder-window-from-one-display-to-another

# BetterChecker3000_v1 = left screen (uses port 40000 for OSC)
# BetterChecker3000_v2 = right screen (uses port 40100 for OSC)


hosts = {
    10: {
        'ip_address': '192.168.0.10',
        'projectors': {
            0: {
                'name': 'top',
                'position': 'right-screen',
                'crop': 0.0,
            },
            1: {
                'name': 'L',
                'position': 'left-screen',
                'crop': 0.0,
            }
        }
    },
    12: {
        'ip_address': '192.168.0.12',
        'projectors': {
            0: {
                'name': 'right',
                'position': 'main',
                'crop': 0.0,
            }
        }
    },
    13: {
        'ip_address': '192.168.0.13',
        'projectors': {
            0: {
                'name': 'regie',
                'position': 'main',
                'crop': 0.0,
            }
        }
    },
    14: {
        'ip_address': '192.168.0.14',
        'projectors': {
            0: {
                'name': 'ceiling',
                'position': 'right-screen',
                'crop': 0.0,
            },
            1: {
                'name': 'left-front',
                'position': 'left-screen',
                'crop': 0.0,
            }
        }
    },
    15: {
        'ip_address': '192.168.0.15',
        'projectors': {
            0: {
                'name': 'stairs',
                'position': 'right-screen',
                'crop': 0.0,
            },
            1: {
                'name': 'right-front',
                'position': 'left-screen',
                'crop': 0.0,
            }
        }
    }
}
