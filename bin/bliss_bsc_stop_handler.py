#!/usr/bin/env python

'''
Usage:
    bliss-bsc-stop-handler [options] <name>

--service-host=<host> The host for the BSC REST service connection
                      [default: localhost]
--service-port=<port> The port for the BSC REST service connection
                      [default: 8080]
'''

from docopt import docopt
import requests


def main():
    arguments = docopt(__doc__)

    host = arguments.pop('--service-host')
    port = arguments.pop('--service-port')

    handler_name = arguments.pop('<name>')

    requests.delete('http://{}:{}/{}/stop'.format(host, port, handler_name))

if __name__ == '__main__':
    main()
