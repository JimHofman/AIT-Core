#!/usr/bin/env python

# Advanced Multi-Mission Operations System (AMMOS) Instrument Toolkit (AIT)
# Bespoke Link to Instruments and Small Satellites (BLISS)
#
# Copyright 2016, by the California Institute of Technology. ALL RIGHTS
# RESERVED. United States Government Sponsorship acknowledged. Any
# commercial use must be negotiated with the Office of Technology Transfer
# at the California Institute of Technology.
#
# This software may be subject to U.S. export control laws. By accepting
# this software, the user agrees to comply with all applicable U.S. export
# laws and regulations. User has the responsibility to obtain export licenses,
# or other export authority as may be required before exporting such
# information to foreign countries or providing access to foreign persons.

'''
Usage:
    bliss-bsc-create-handler [options] <name> <loc> <port> <conn_type>

--service-host=<host> The host for the BSC REST service connection
                      [default: localhost]
--service-port=<port> The port for the BSC REST service connection
                      [default: 8080]
--rotate=<rl>         Flag saying whether the log should be rotated
                      automatically [default: True]
--rotate-index=<rli>  If log rotation is enabled, this determines the
                      frequency of a rotation. One of 'year', 'month',
                      'day', 'hour', 'minutes', 'second' [default: day]
--rotate-delta=<rld>  If log rotation is enabled, this determines the
                      delta between log creation and current time
                      rotate-index value needed to trigger a log
                      rotation [default: 1]
--file-pattern=<fnp>  The file pattern for the log file name. This can
                      include handler metadata values as well as strftime
                      format characters [default: %Y-%m-%d-%H-%M-%S-{name}.pcap]
'''

import argparse
import requests

def main():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)

    # Add required command line arguments
    parser.add_argument('name')
    parser.add_argument('loc')
    parser.add_argument('port', type=int)
    parser.add_argument('conn_type')

    # Add optional command line arguments
    parser.add_argument('--service-host', default='localhost')
    parser.add_argument('--service-port', type=int, default=8080)
    parser.add_argument('--rotate', type=int, default=1)
    parser.add_argument('--rotate-index', choices=['year','month','day','hour','minutes','second'], default='day')
    parser.add_argument('--rotate-delta', type=int, default=1)
    parser.add_argument('--file-pattern', default='\%Y-\%m-\%d-\%H-\%M-\%S-{name}.pcap')

    # Get command line arguments
    args = vars(parser.parse_args())

    host = args['service-host']
    port = args['service-port']

    handler_name = args['name']

    handler_port = args['port']
    arguments['port'] = handler_port

    handler_conn_type = args['conn_type']
    arguments['conn_type'] = handler_conn_type

    handler_loc = args['loc']
    arguments['loc'] = handler_loc

    arguments['rotate_log'] = eval(args['rotate'])
    arguments['rotate_log_index'] = args['rotate-index']
    arguments['rotate_log_delta'] = args['rotate-delta']
    arguments['file_name_pattern'] = args['file-pattern']

    requests.post(
        'http://{}:{}/{}/start'.format(host, port, handler_name),
        data=arguments
    )

if __name__ == '__main__':
    main()
