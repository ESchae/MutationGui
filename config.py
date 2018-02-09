basepath = '/Users/mutation/Desktop/Mutation2018/'
desktoppath = '/Users/mutation/Desktop/'

groups = {
    'TeamTest': {
        # globals
        'use_checker': True,
        # for each projector, specify which app should be run
        'projector_settings': {
            'top': {
                'app': 'xy.app',
                'syphon_server': '123'
            }
        }
    },
    'MarninTobi': {
        # globals
        'use_checker': False,
        # for each projector, specify which app should be run
        'projector_settings': {
            'top': {
                'app': 'xy.app',
                'syphon_server': None
            }
        }
    }
}

# projector name = name to describe its shape /find it in MUT
# projector position = monitor position
# important note: name of corresponding checker app for a specific projector will be
# derived as follows: checker_<name>_<position>/checker3.app !

# right-screen must be listed before left-screen!

hosts = {
    10: {
        'ip_address': '192.168.0.10',
        'projectors': {
            0: {
                'name': 'top',
                'position': 'right-screen',
                'port': 5000,
            },
            1: {
                'name': 'L',
                'position': 'left-screen',
                'port': 5001,
            }
        }
    },
    12: {
        'ip_address': '192.168.0.12',
        'projectors': {
            0: {
                'name': 'dummy1',
                'position': 'oben',
                'port': 5000,
            },
            1: {
                'name': 'dummy1',
                'position': 'oben',
                'port': 5000,
            }
        }
    },
    13: {
        'ip_address': '192.168.0.13',
        'projectors': {
            0: {
                'name': 'foh',
                'position': '-',
                'port': 5000,
            }
        }
    },
    14: {
        'ip_address': '192.168.0.14',
        'projectors': {
            0: {
                'name': 'neben foh',
                'position': 'links',
                'port': 5000,
            },
            1: {
                'name': 'decke',
                'position': 'rechts',
                'port': 5000,
            }
        }
    },
    15: {
        'ip_address': '192.168.0.15',
        'projectors': {
            0: {
                'name': 'treppe',
                'position': 'oben',
                'port': 5000,
            },
            1: {
                'name': 'links von L',
                'position': 'oben',
                'port': 5000,
            }
        }
    }
}
