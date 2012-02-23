# coding: utf8

#  WeasyPrint converts web documents (HTML, CSS, ...) to PDF.
#  Copyright (C) 2011  Simon Sapin
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as
#  published by the Free Software Foundation, either version 3 of the
#  License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.


"""
Command-line interface to WeasyPrint.

"""

from __future__ import division, unicode_literals

import sys
import argparse

from . import VERSION, HTML


def main(argv=None):
    """Parse command-line arguments and convert the given document."""
    format_values = ['pdf', 'png']
    formats = 'PDF or PNG'
    extensions = '.pdf or .png'

    parser = argparse.ArgumentParser(prog='weasyprint',
        description='Renders web pages into ' + formats)
    parser.add_argument('--version', action='version',
                        version='WeasyPrint version %s' % VERSION,
                        help='Print WeasyPrint’s version number and exit.')
    parser.add_argument('-e', '--encoding',
                        help='Character encoding of the input')
    parser.add_argument('-f', '--format', choices=format_values,
                        help='Output format. Can be ommited if `output` '
                             'ends with ' + extensions)
    parser.add_argument('-s', '--stylesheet', action='append',
                        help='Apply a user stylesheet to the document. '
                             'May be given multiple times.')
    parser.add_argument('input',
        help='URL or filename of the HTML input, or - for stdin')
    parser.add_argument('output',
        help='Filename where output is written, or - for stdout')

    args = parser.parse_args(argv)

    if args.format is None:
        for file_format in format_values:
            if args.output.endswith('.' + file_format):
                args.format = file_format
                break
        else:
            parser.error(
                'Either sepecify a format with -f or choose an '
                'output filename that ends in ' + extensions)

    if args.input == '-':
        stdin = sys.stdin
        stdin = getattr(stdin, 'buffer', stdin)
        source = HTML(file_obj=stdin, encoding=args.encoding,
            # Dummy filename in the current directory.
            base_url='<stdin>')
    else:
        source = HTML(args.input, encoding=args.encoding)

    if args.output == '-':
        stdout = sys.stdout
        stdout = getattr(stdout, 'buffer', stdout)
        args.output = stdout

    getattr(source, 'write_' + args.format)(
        args.output, stylesheets=args.stylesheet)


if __name__ == '__main__':
    main()
