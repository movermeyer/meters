import sys
import os
import re
import socket
import platform
import functools
import time


##### Public methods #####
def get_app():
    name = os.path.basename(sys.argv[0]) # Strip path
    name = re.sub(r"\.py[cow]?$", "", name) # Strip ".py?" ending
    return name

def get_node():
    return platform.uname()[1]

def get_fqdn(refresh_every=60):
    return _cached_getfqdn(int(time.time() / refresh_every))


##### Private methods #####
@functools.lru_cache(1)
def _cached_getfqdn(refresh_every):
    return socket.getfqdn()

