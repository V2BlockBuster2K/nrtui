import json
import os
import sys


def get_config_dir():
    return '/home/' + os.getlogin() + '/.config/nrtui'


def check_dir():
    conf = get_config_dir()
    if os.path.exists(conf):
        if os.path.exists(conf + '/settings.json'):
            return True
        else:
            with open(conf + '/settings.json', 'w') as file:
                json.dump(
                    {'default': {'ads': False, 'delay': '1', 'offset': '2'}}, file)
            check_dir()
    else:
        os.makedirs(conf)
        check_dir()


def run_as_root():
    euid = os.geteuid()
    if euid != 0:
        args = ['sudo', sys.executable] + sys.argv + [os.environ]
        # the next line replaces the currently-running process with the sudo
        os.execlpe('sudo', *args)
