#!/usr/bin/env python3
#
# args.py
#
# Copyright (C) 2014 - Wiky L
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#

#解析命令行参数

import os

class InvalidArgs(Exception):
    pass

class Parser:
    def __init__(self,argv):
        self.input=None
        self.output=None
        try:
            self.input=argv[1]
            self.output=argv[2]
        except Exception as e:
            if self.input is None:
                raise InvalidArgs("input file must be specified!")
            elif not os.path.isfile(self.input):
                raise InvalidArgs("input file "+self.input+" is not available")

        if self.output is None:
            # 如果未指定输出文件，则根据输入文件在当前目录下创建一个
            file=os.path.basename(self.input)
            i=file.rfind(".")
            if i > 0 :
                file=file[:i]
                file=file+".java"
            self.output="./"+file

        print("INPUT:\t{0}\nOUTPUT:\t{1}".format(self.input,self.output))



def show_help():
    print("Usage:\txmlcode.py input.xml [output.java]")
    print("\tinput.xml\tthe XML file that specifies the layout")
    print("\t\t\tof Android UI components")
    print("\toutput.java\tthe file to save the generated JAVA code")

def show_help_and_exit(code=0):
    show_help()
    exit(code)

def show_help_with_exception(e):
    print(e,"\n")
    show_help_and_exit()
