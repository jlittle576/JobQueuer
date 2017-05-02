import sys, os, shutil, glob, copy, time, datetime, inspect, re, random, math, subprocess
from collections import OrderedDict
from dateutil import tz


# --- setting_constants ---
def setting_constants(): return

ADAMS_START_LIMIT = 60
ADAMS_FINISH_LIMIT = 60 * 60
SPOOF_RUN_TIME = 8

# --- term constants  --
def term_constants(): return

# job status definitions
QUEUED = 'QUEUED'
RUNNING = 'RUNNING'
COMPLETE = 'COMPLETE'
FAILED = 'FAILED'
TIMED_OUT = 'TIMED_OUT'
WAITING_FOR_TRANSFER_COMPLETION = 'WAITING_FOR_TRANSFER_COMPLETION'

# sub status
WAITING_FOR_ADAMS_START = 'WAITING_FOR_ADAMS_START'
MONITORING_ADAMS_LOG = 'MONITORING_ADAMS_LOG'
INITIALIZED = 'INITIALIZED'

# run modes
RUN_TEST = 'RUN_TEST'
RUN_TEST_STATIC = 'RUN_TEST_STATIC'
RUN_TEST_TRANSFER_WAIT = 'RUN_TEST_TRANSFER_WAIT'
RUN_PROD = 'RUN_PROD'

# run types
SINGLE = 'Single'
FULL = 'Full'

# run settings
SPOOF_SINGLE = 'SPOOF_SINGLE'
SPOOF_DOE = 'SPOOF_DOE'
RUN_SINGLE = 'RUN_SINGLE'
RUN_DOE = 'RUN_DOE'

DOE_COMPLETE_STRING = 'RUNSTUDY COMPLETE'
SINGLE_COMPLETE_STRING = 'Information: Model creation complete'


# --- sentinels ---
def sentinels(): return

TEST_TRANSFER_WAIT = False
TEST_QUE_MOD = False
TEST_QUE_ADD = False


# --- utility_functions ---
def utility_functions(): return

def open_explorer(path):
    path = path.replace('/', '\\')
    subprocess.Popen(r'explorer %s' % path,
                     shell=True)

def kill_adams():
    os.system('start taskkill.exe /F /IM aview* /T')

def fl_get(term):
    return slash_fix(glob.glob(term))

def get_dir_size(path):
    total_size = -1
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)

    if total_size  == -1:
        _ = 0
    return total_size

def time_now():
    return datetime.datetime.now()

def seconds_since(dt):
    return (datetime.datetime.now() - dt).total_seconds()

f_add = lambda x, y: f_mod(x, 'a', y)
f_write = lambda x, y: f_mod(x, 'w', y)
f_read = lambda x: f_mod(x, 'r')
f_clear = lambda x: f_mod(x, 'w')


def f_mod(path, mode, text=''):
    vars = inspect.stack()[1][0].f_locals
    path = path % vars
    fOut = open(path, mode)
    if mode in ['a', 'w']:
        fOut.write(text)
    else:
        text = fOut.read()
    fOut.close()
    return text if mode == 'r' else None


def slash_fix(paths):
    return_str = False
    if type(paths) is str:
        paths = [paths]
        return_str = True

    new_paths = []
    for path in paths:
        new_path = path.replace('\\', '/')
        if '\\' in new_path:
            raise Exception('slash_fix failes!' + new_path)
        else:
            new_paths.append(new_path)

    if return_str:
        return new_paths[0]
    else:
        return new_paths