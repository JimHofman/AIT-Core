#!/usr/bin/env python

# Advanced Multi-Mission Operations System (AMMOS) Instrument Toolkit (AIT)
# Bespoke Link to Instruments and Small Satellites (BLISS)
#
# Copyright 2013, by the California Institute of Technology. ALL RIGHTS
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
usage: bliss-yaml-validate

Validate YAML files with applicable schema and/or advanced
content validation for CMD and TLM dictionaries.

YAML validation is done through a combination of JSON Schema
(http://json-schema.org/) and Python-coded content validation.
The JSON Schema is used to validate general format of the YAML,
i.e dictionaries contain the expected keys, values are the
expected type, etc.

Why JSON Schema? All of the available YAML validators did not
meet the robustness expected for this tool. Since JSON and YAML
are stored similarly in memory, the JSON Schema became an option.
The only difference between YAML and JSON is the use of multiple
documents in the same YAML file. The val.py module handles this
implication. See TBD wiki page for more details on developing
JSON schema for an applicable YAML file.

Examples:

  $ bliss-yaml-validate --cmd
  $ bliss-yaml-validate --tlm
  $ bliss-yaml-validate --evr
  $ bliss-yaml-validate --cmd --yaml /path/to/cmd.yaml
  $ bliss-yaml-validate --tlm --yaml /path/to/tlm.yaml
  $ bliss-yaml-validate --yaml /path/to/yaml --schema /path/to/schema
'''


import argparse
import os
import sys
import textwrap

import bliss
from bliss.core import cmd, evr, log, tlm, val, limits


def validate(validator, yml, schema):
    msgs      = []
    validator = validator(yml, schema)
    valid     = validator.validate(messages=msgs)

    msg = "Validation: %s: yml=%s, schema=%s"

    if valid:
        log.info(msg % ('SUCCESS', yml, schema))
        return 0
    else:
        log.error(msg % ('FAILED', yml, schema))
        for msg in msgs:
            log.error(msg)
        return 1


def main():
    argparser = argparse.ArgumentParser(
        description = """
Validate YAML files with applicable schema and/or advanced
content validation for CMD and TLM dictionaries.

YAML validation is done through a combination of JSON Schema
(http://json-schema.org/) and Python-coded content validation.  The
JSON Schema is used to validate general format of the YAML, i.e
dictionaries contain the expected keys, values are the expected type,
etc.

Why JSON Schema? All of the available YAML validators did not meet the
robustness expected for this tool. Since JSON and YAML are stored
similarly in memory, the JSON Schema became an option.  The only
difference between YAML and JSON is the use of multiple documents in
the same YAML file. The val.py module handles this implication. See
TBD wiki page for more details on developing JSON schema for an
applicable YAML file.
""",
        epilog = """
Examples:

    $ bliss-yaml-validate.py --cmd
    $ bliss-yaml-validate.py --tlm
    $ bliss-yaml-validate.py --evr
    $ bliss-yaml-validate.py --cmd --yaml /path/to/cmd.yaml
    $ bliss-yaml-validate.py --tlm --yaml /path/to/tlm.yaml
    $ bliss-yaml-validate.py --yaml /path/to/yaml --schema /path/to/schema
""",
        formatter_class = argparse.RawDescriptionHelpFormatter
    )

    argparser.add_argument(
        '-y', '--yaml',
        metavar = '</path/to/yaml>',
        type    = str,
        help    = 'Path to YAML file.'
    )

    argparser.add_argument(
        '-s', '--schema',
        metavar = '</path/to/schema>',
        type    = str,
        help    = 'Path to JSON schema file.'
    )

    argparser.add_argument(
        '-c', '--cmd',
        action  = 'store_true',
        default = False,
        help    = """Command dictionary flag. If a YAML file is not
        specified, the default command dictionary and schema will be used.
        """
    )

    argparser.add_argument(
        '-t', '--tlm',
        action  = 'store_true',
        default = False,
        help    = """Telemetry dictionary flag. If a YAML file is not
        specified, the default telemetry dictionary and schema will be used.
        """
    )

    argparser.add_argument(
        '-e', '--evr',
        action  = 'store_true',
        default = False,
        help    = """EVR dictionary flag. If a YAML file is not specified,
        the default EVR dictionary and schema will be used.
        """
    )

    argparser.add_argument(
        '-l', '--limits',
        action  = 'store_true',
        default = False,
        help    = """Limits dictionary flag. If a YAML file is not specified,
        the default limits dictionary and schema will be used.
        """
    )    

    if len(sys.argv) < 2:
        argparser.print_usage()
        print 'Run with --help for detailed help.'
        sys.exit(2)

    options = argparser.parse_args()

    log.begin()

    # Validate specified yaml file with specified schema
    if options.yaml is not None and options.schema is not None:
        # Check YAML exists
        if not os.path.exists(options.yaml):
            raise os.error(options.yaml + " does not exist.")

        # Check schema exists
        if not os.path.exists(options.schema):
            raise os.error(options.schema + " does not exist.")

        validator = val.Validator
        retcode = validate(validator, options.yaml, options.schema)

    else:
        if options.cmd:
            yml       = bliss.config.cmddict.filename
            schema    = cmd.getDefaultSchema()
            validator = val.CmdValidator
        elif options.evr:
            yml       = bliss.config.evrdict.filename
            schema    = evr.getDefaultSchema()
            validator = val.Validator
        elif options.tlm:
            yml       = bliss.config.tlmdict.filename
            schema    = tlm.getDefaultSchema()
            validator = val.TlmValidator
        elif options.limits:
            yml       = bliss.config.limits.filename
            schema    = limits.getDefaultSchema()
            validator = val.Validator

        if options.yaml is not None:
            yml = options.yaml

        retcode = validate(validator, yml, schema)

    log.end()
    return retcode


if __name__ == "__main__":
    main()
