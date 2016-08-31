#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import click

@click.command()

import os


from argparse import ArgumentParser

from steenzout import barcode
from steenzout.barcode import metadata
from steenzout.barcode.writer import ImageWriter, SVG

try:
    import PIL
    PIL_ENABLED = True
except ImportError:
    PIL_ENABLED = False

IMG_FORMATS = ('BMP', 'GIF', 'JPEG', 'MSP', 'PCX', 'PNG', 'TIFF', 'XBM')


def list_types():
    print('\npyBarcode available barcode formats:')
    print(', '.join(barcode.PROVIDED_BAR_CODES))
    print('\n')
    print('Available image formats')
    print('Standard: svg')
    if PIL_ENABLED:
        print('PIL:', ', '.join(IMG_FORMATS))
    else:
        print('PIL: disabled')
    print('\n')


def create_barcode(args, parser):
    args.type = args.type.upper()
    if args.type != 'SVG' and args.type not in IMG_FORMATS:
        parser.error('Unknown type {type}. Try list action for available '
                     'types.'.format(type=args.type))
    args.barcode = args.barcode.lower()
    if args.barcode not in barcode.PROVIDED_BAR_CODES:
        parser.error('Unknown barcode {bc}. Try list action for available '
                     'barcodes.'.format(bc=args.barcode))
    if args.type != 'SVG':
        opts = dict(format=args.type)
        writer = ImageWriter()
    else:
        opts = dict(compress=args.compress)
        writer = SVG()
    out = os.path.normpath(os.path.abspath(args.output))
    name = barcode.generate(args.barcode, args.code, writer, out, opts)
    print('New barcode saved as {0}.'.format(name))


def main():
    msg = []
    if ImageWriter is None:
        msg.append('Image output disabled (PIL not found), --type option '
                   'disabled.')
    else:
        msg.append('Image output enabled, use --type option to give image '
                   'format (png, jpeg, ...).')

    parser = ArgumentParser(
        description=metadata.__description__,
        epilog=' '.join(msg))
    parser.add_argument(
        '-v', '--version',
        action='version',
        version='%(prog)s ' + metadata.__release__)
    subparsers = parser.add_subparsers(title='Actions')
    create_parser = subparsers.add_parser(
        'create',
        help='Create a barcode with the given options.')
    create_parser.add_argument(
        'code',
        help='Code to render as barcode.')
    create_parser.add_argument(
        'output',
        help='Filename for output without extension, e.g. mybarcode.')
    create_parser.add_argument(
        '-c', '--compress',
        action='store_true',
        help='Compress output, only recognized if type is svg.')
    create_parser.add_argument(
        '-b', '--barcode',
        help='Barcode to use [default: %(default)s].')
    if ImageWriter is not None:
        create_parser.add_argument(
            '-t', '--type',
            help='Type of output [default: %(default)s].')
    list_parser = subparsers.add_parser(
        'list', help='List available image and code types.')
    list_parser.set_defaults(func=list_types)

    create_parser.set_defaults(
        barcode='code39',
        compress=False,
        func=create_barcode,
        type='svg')

    args = parser.parse_args()
    args.func(args, parser)


if __name__ == '__main__':
    main()