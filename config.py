
groups = ['TeamTest', 'Alessandro', 'MarninTobi']

basepath = '/Users/mutation/Desktop/Mutation2018/'


hosts = {
    10: {
        'ip_address': '192.168.10',
        'projectors': {
            0: {
                'name': 'L',
                'position': 'left',
                'checker_app': 'Checker-0-L',
                'port': 5000,
            },
            1: {
                'name': 'Hoechstes Gelaender',
                'position': 'rechts',
                'checker_app': 'Checker',
                'port': 5010,
            }
        }
    },
    11: {
        'ip_address': '192.168.11',
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
    12: {
        'ip_address': '192.168.12',
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
        'ip_address': '192.168.13',
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
        'ip_address': '192.168.14',
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
        'ip_address': '192.168.15',
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