#!/usr/bin/env python

""" Example of announcing a service (in this case, a fake HTTP server) """

import logging
import socket
import sys
from time import sleep

from zeroconf import ServiceInfo, Zeroconf

if __name__ == '__main__':
    info = ServiceInfo("_http._tcp.local.",
                       "Who Am I._http._tcp.local.",
                       80, 0, 0,
                       {'name': "whoami"}, "whoami.local.")

    zeroconf = Zeroconf()
    print("Registration of a service, press Ctrl-C to exit...")
    zeroconf.register_service(info)
    try:
        while True:
            sleep(20)
    except KeyboardInterrupt:
        pass
    finally:
        zeroconf.close()