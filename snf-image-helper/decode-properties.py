#!/usr/bin/env python

"""Decode a json encoded string with properties

This program decodes a json encoded properties string and outputs it in a
bash sourcable way. The properties are passed to the program through a JSON
string either read from a file or from standard input and are outputed to a
target file.
"""

import sys
import os
import subprocess
import json
from StringIO import StringIO
from optparse import OptionParser

def parse_arguments(input_args):
    usage = "Usage: %prog [options] <output_file>"
    parser = OptionParser(usage=usage)
    parser.add_option("-i", "--input",
                        action="store",type='string', dest="input_file",
                        help="get input from FILE instead of stdin",
                        metavar="FILE")

    opts, args = parser.parse_args(input_args)

    if len(args) != 1:
        parser.error('output file is missing')
    output_file = args[0]
   
    if opts.input_file is not None:
        if not os.path.isfile(opts.input_file):
            parser.error('input file does not exist')
 
    return (opts.input_file, output_file)


def main():
    (input_file, output_file) = parse_arguments(sys.argv[1:])

    infh = sys.stdin if input_file is None else open(input_file, 'r')
    outfh = open(output_file, 'w')

    properties = json.load(infh)
    for key, value in properties.items():
        os.environ['SNF_IMAGE_PROPERTY_' + key] = value

    p = subprocess.Popen(['bash', '-c', 'set'], stdout=subprocess.PIPE)
    output = StringIO(p.communicate()[0]);
    for line in iter(output):
        if line.startswith('SNF_IMAGE_PROPERTY_'):
            outfh.write('export ' + line)

    infh.close()
    outfh.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())

# vim: set sta sts=4 shiftwidth=4 sw=4 et ai :