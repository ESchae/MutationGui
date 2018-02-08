
groups = ['TeamTest', 'Alessandro', 'MarninTobi']

basepath = '/Users/mutation/Desktop/Mutation2018/'
desktoppath = '/Users/mutation/Desktop/'

# projector name = name to describe its shape /find it in MUT
# projector position = monitor position

hosts = {
    10: {
        'ip_address': '192.168.0.10',
        'projectors': {
            0: {
                'name': 'L',
                'position': 'left',
                'checker_app': 'checker-0-L',
                'port': 5000,
            },
            1: {
                'name': 'Hoechstes Gelaender',
                'position': 'rechts',
                'checker_app': 'checker-1-Oben',
                'port': 5010,
            }
        }
    },
    12: {
        'ip_address': '192.168.0.12',
        'projectors': {
            0: {
                'name': 'dummy1',
                'position': 'oben',
                'checker_app': 'Checker-0-L',
                'port': 5000,
            },
            1: {
                'name': 'dummy1',
                'position': 'oben',
                'checker_app': 'Checker-0-L',
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
                'checker_app': 'Checker-0-L',
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
                'checker_app': 'Checker-0-L',
                'port': 5000,
            },
            1: {
                'name': 'decke',
                'position': 'rechts',
                'checker_app': 'Checker-0-L',
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
                'checker_app': 'Checker-0-L',
                'port': 5000,
            },
            1: {
                'name': 'links von L',
                'position': 'oben',
                'checker_app': 'Checker-0-L',
                'port': 5000,
            }
        }
    }
}
