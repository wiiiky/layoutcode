#!/usr/bin/env python3
#
# xxml.py
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


# 解析XML文件相关

import xml.etree.ElementTree as ET


tmp_index=0
def get_tmp_name():
    """返回一个类似tmp0，tmp1这样的变量名"""
    global tmp_index
    tmp_index=tmp_index+1
    return "tmp" + str(tmp_index)

class View:
    """一个节点的基本属性处理"""
    def __init__(self,e, parent=None,parent_id=None):
        parent_type="ViewGroup"
        if parent is not None:
            parent_type=parent.tag
        type=e.tag
        id=None
        margin_left=None
        margin_right=None
        margin_top=None
        margin_bottom=None
        text=None
        layout_weight=None
        layout_width="ViewGroup.LayoutParams.WRAP_CONTENT"
        layout_height="ViewGroup.LayoutParams.WRAP_CONTENT"
        fillViewport=None
        orientation=None
        for k,v in e.items():
            key=self.handle_key(k)
            value=self.handle_value(v)
            if key=="id":
                id=self.convert_id(value)
            elif key=="layout_width":
                layout_width=self.convert_layout(value)
            elif key=="layout_height":
                layout_height=self.convert_layout(value)
            elif key=="layout_weight":
                layout_weight=value
            elif key=="layout_marginleft":
                margin_left=self.convert_dp(value)
            elif key=="layout_marginright":
                margin_right=self.convert_dp(value)
            elif key=="layout_margintop":
                margin_top=self.convert_dp(value)
            elif key=="layout_marginbottom":
                margin_bottom=self.convert_dp(value)
            elif key=="text":
                text=value;
            elif key=="fillviewport":
                fillViewport=value
            elif key=="orientation":
                orientation=self.convert_orientation(value)
            else:
                print("unkonwn : " +key + "|" + value)
        
        if id is None:
            id=get_tmp_name()

        var=str(id)
        params=var + "Params"
        margins=var + "Margins"
        code=[]
        code.append(type + " "+str(id) + " = new " + type + "(this);")
        if margin_left or margin_right or margin_top or margin_bottom:
            margin_left=margin_left or "0"
            margin_top=margin_top or "0"
            margin_right=margin_right or "0"
            margin_bottom=margin_bottom or "0"
            code.append("MarginLayoutParams "+margins+" = new MarginLayoutParams" +layout_width+","+layout_height+");")
            code.append(margins + ".setMargins(" + margin_left+ ","+margin_top+","+margin_right+","+margin_bottom+");")
            code.append(parent_type + ".LayoutParams "+params + " = new " + parent_type + ".LayoutParams("+margins+");")
        else:
            code.append(parent_type + ".LayoutParams "+params + " = new " + parent_type + ".LayoutParams("+layout_width+","+layout_height+");")

        if layout_weight is not None:
            code.append(params + ".weight=" + layout_weight + ";")

        code.append(var + ".setLayoutParams(" + params + ");")

        if text is not None and len(text)>0:
            code.append(var + ".setText(\"" + text + "\");")

        if fillViewport is not None:
            code.append(var + ".setFillViewport(" + fillViewport + ");")

        if orientation is not None:
            code.append(var + ".setOrientation(" + orientation +");")

        if parent_id:
            code.append(parent_id + ".addView(" + id +");")

        code.append("\n")

        self.id=id
        self.code=code

    def convert_layout(self,v):
        value=v.lower()
        if value=="fill_parent" or value=="match_parent":
            return "ViewGroup.LayoutParams.MATCH_PARENT"
        elif value=="wrap_parent":
            return "ViewGroup.LayoutParams.WRAP_CONTENT"
        return self.convert_dp(value);

    def convert_dp(self,v):
        if v.endswith("dp"):
            return str(int(v[:-2]))
        i=v.find("dimen/")
        if i>=0:
            return "getResources().getDimension(R.dimen."+ v[i+6:] +")"
        return "0"

    def convert_id(self,v):
        i=v.find("/")
        if i>0:
            return v[i+1:]
        return v

    def convert_orientation(self, v):
        lower=v.lower()
        if lower=="vertical":
            return "LinearLayout.VERTICAL"
        return "LinearLayout.HORIZONTAL"

    def handle_key(self,key):
        right=key.find("}")
        result=key
        if right>0:
            result=key[right+1:]
        return result.lower()

    def handle_value(self,value):
        return value
        
    

class Generator:
    """docstring for Generator"""
    def __init__(self, data):
        tree=ET.ElementTree(file=data.input)
        self.root=tree.getroot()

        self.for_all(self.root);

    def for_all(self,root,p=None,pid=None):
        """处理所有子节点"""

        view=View(root,p,pid)
        for s in view.code:
            print(s)

        children=root.getchildren()
        if children is not None:
            for i in children:
                self.for_all(i,root,view.id)

        if p is None:   # 返回根节点
            print("return " + view.id +";")

    def handle_linearlayout(self,e,p):
        """处理LinearLayout"""
        View(e,p)
