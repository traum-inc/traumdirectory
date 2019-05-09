from configparser import ConfigParser

config = ConfigParser()

config['log'] = {
    'stderr': False,
    'color': False,
    'file': '',
    'append': True,
    'level': 'debug',
    }

config.read('config.ini')
