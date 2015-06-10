#!/usr/bin/env python3
# encoding=utf8

import argparse


parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', help='Input filepath.')
parser.add_argument('-o', '--output', help='Output filepath. ')
args = parser.parse_args()

print(args.input)
