#!/usr/bin/env python3
# encoding=utf8

import argparse
import sys
from bs4 import BeautifulSoup
from widget import *


parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', help='Input filepath.')
parser.add_argument('-o', '--output', help='Output filepath. ')
args = parser.parse_args()

if args.input:
    src = open(args.input, 'r')
else:
    src = sys.stdin

if args.output:
    dst = open(args.output, 'w')
else:
    dst = sys.stdout

data = src.read()
soup = BeautifulSoup(data, 'xml')

root = soup.findChild()

v = create_view(root)
print(str(v))
