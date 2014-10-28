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

def list_contains(list,v):
    for i in list:
        if i==v:
            return True
    return False

class View:
    """一个节点的基本属性处理"""
    def __init__(self,e, parent=None,parent_id=None):
        self_type=e.tag

        parent_type="ViewGroup"
        if parent is not None:
            parent_type=parent.tag

        margin_left=None
        margin_right=None
        margin_top=None
        margin_bottom=None
        layout_weight=None
        layout_width="ViewGroup.LayoutParams.WRAP_CONTENT"
        layout_height="ViewGroup.LayoutParams.WRAP_CONTENT"

        paddingLeft=None
        paddingRight=None
        paddingTop=None
        paddingBottom=None
        paddingStart=None
        paddingEnd=None
        
        id=None
        #先找到id
        for k,v in e.items():
            key=self.handle_key(k)
            value=self.handle_value(v)
            if key=="id":
                id=self.convert_id(value)
                break

        if id is None:
            id=get_tmp_name()

        ignored=["id","context"]    # 忽略的属性

        var=str(id)
        params=var + "Params"
        margins=var + "Margins"

        code=[]
        code.append(self_type + " "+str(id) + " = new " + self_type + "(this);")

        for k,v in e.items():
            key=self.handle_key(k)
            value=self.handle_value(v)
            if key=="layout_width":
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
            elif key=="paddingleft":
                paddingLeft=self.convert_dp(value)
            elif key=="paddingright":
                paddingRight=self.convert_dp(value)
            elif key=="paddingtop":
                paddingTop=self.convert_dp(value)
            elif key=="paddingbottom":
                paddingBottom=self.convert_dp(value)
            elif key=="paddingstart":
                paddingStart=self.convert_dp(value)
            elif key=="paddingend":
                paddingEnd=self.convert_dp(value)
            elif key=="padding":
                padding=self.convert_dp(value)
                paddingLeft=padding
                paddingRight=padding
                paddingTop=padding
                paddingBottom=padding
            elif key=="gravity":
                gravity=self.convert_gravity(value)
                code.append(var + ".setGravity(" + gravity + ");" )
            elif key=="text":    #TextView Button
                if len(value)>0:
                    text=self.convert_text(value)
                    code.append(var + ".setText(" + text + ");")
            elif key=="textcolor":
                color=self.convert_color(value)
                code.append(var + ".setTextColor(" + color +");")
            elif key=="textcolorlink":
                color=self.convert_color(value)
                code.append(var + ".setLinkTextColor(" + color + ");")
            elif key=="singleline":
                code.append(var + ".setSingleLine(" + value + ");")
            elif key=="fillviewport": #ScrollView
                code.append(var + ".setFillViewport(" + value + ");")
            elif key=="orientation":
                orientation=self.convert_orientation(value)
                code.append(var + ".setOrientation(" + orientation +");")
            elif key=="src":  #ImageView
                src=self.convert_src(value)
                code.append(var + ".setImageDrawable(" + src + ");")
            elif key=="background":
                bg=self.convert_background(value)
                code.append(var + ".setBackgroundResource(" + bg + ");")
            elif key=="style":
                style=self.convert_style(value)
                code.append(self.get_style_code(self_type,var,style))
            elif key=="completionthreshold":
                code.append(var + ".setThreshold(" + value + ");")
            elif not list_contains(ignored,key):
                print("unkonwn : " +key + "|" + value)

        if paddingLeft or paddingRight or paddingTop or paddingBottom:
            left=paddingLeft or "0"
            right=paddingRight or "0"
            top=paddingTop or "0"
            bottom=paddingBottom or "0"
            code.append(var + ".setPadding((int)" + left +",(int)" + top + ",(int)" + right + ",(int)" + bottom + ");")
        elif paddingStart or paddingEnd or paddingTop or paddingBottom:
            start=paddingStart or "0"
            end=paddingEnd or "0"
            top=paddingTop or "0"
            bottom=paddingBottom or "0"
            code.append(var + ".setPaddingRelative((int)" + start + ",(int)" + top + ",(int)" + end + ",(int)" + bottom + ");")

        if margin_left or margin_right or margin_top or margin_bottom:
            margin_left=margin_left or "0"
            margin_top=margin_top or "0"
            margin_right=margin_right or "0"
            margin_bottom=margin_bottom or "0"
            code.append("ViewGroup.MarginLayoutParams "+margins+" = new ViewGroup.MarginLayoutParams(" +layout_width+","+layout_height+");")
            code.append(margins + ".setMargins(" + margin_left+ ","+margin_top+","+margin_right+","+margin_bottom+");")
            code.append(parent_type + ".LayoutParams "+params + " = new " + parent_type + ".LayoutParams("+margins+");")
        else:
            code.append(parent_type + ".LayoutParams "+params + 
                    " = new " + parent_type + ".LayoutParams("+layout_width+","+layout_height+");")

        if layout_weight is not None:
            code.append(params + ".weight=" + layout_weight + ";")

        code.append(var + ".setLayoutParams(" + params + ");")

        if parent_id:
            code.append(parent_id + ".addView(" + id +");")

        self.id=id
        self.code=code

    def convert_layout(self,v):
        value=v.lower()
        if value=="fill_parent" or value=="match_parent":
            return "ViewGroup.LayoutParams.MATCH_PARENT"
        elif value=="wrap_content":
            return "ViewGroup.LayoutParams.WRAP_CONTENT"
        return self.convert_dp(value);

    def convert_gravity(self,v):
        if v=="center_horizontal":
            return "Gravity.CENTER_HORIZONTAL"
        elif v=="center_vertical":
            return "Gravity.CENTER_VERTICAL"
        return "Gravity.CENTER"

    def convert_src(self,v):
        i=v.find("drawable/")
        if i>=0:
            return "getResources().getDrawable(R.drawable."+ v[i+9:] +")"
        return "unknown";

    def convert_background(self,v):
        i=v.find("drawable/")
        if i>=0:
            return "R.drawable." + v[i+9:]
        i=v.find("color/")
        if i>=0:
            return "R.color." + v[i+6:]
        return "unknown"

    def convert_style(self,v):
        i=v.find("style/")
        if i>=0:
            return "R.style." + v[i+6:]
        return "unknown"

    def convert_text(self,v):
        i=v.find("string/")
        if i>=0:
            return "getResources().getString(R.string."+ v[i+7:]  +")"
        return "\"" + v + "\""

    def convert_color(self,v):
        i=v.find("color/")
        if i>=0:
            return "getResources().getColor(R.color."+ v[i+6:] + ")"
        return "unknown"

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
    
    def get_style_code(self,self_type,var,style):
        if self_type=="TextView" or self_type=="CheckBox" or self_type=="EditText" or self_type=="AutoCompleteTextView":
            return var + ".setTextAppearance(this," + style + ");"

        return "[style?]"


class Generator:
    """docstring for Generator"""
    def __init__(self, data):

        try:
            tree=ET.ElementTree(file=data.input)
            self.root=tree.getroot()
        except Exception as e:
            print(e)
            return

        # 将所有节点按处理顺序保存在self.views数组中
        self.views=[]
        self.for_all(self.root);


        all=""
        for view in self.views:
            for s in view.code:
                all=all + s + "\n"
            all=all+"\n"
            
        #后期处理
        i=all.find("getResources()")
        if i>=0:    # 如果用到getResources()那么，将其提取出来，避免重复调用
            res="res"
            all=all.replace("getResources()",res)
            all="Resources " +res + " = getResources();\n\n" + all

        try:    # 写入文件
            file=open(data.output,"w")
            file.write(all)
            file.write("return " + self.views[0].id + ";\n")
            file.close()
        except Exception as e:
            print(e)
            return
        print("Success!")

    def for_all(self,root,p=None,pid=None):
        """处理所有子节点"""

        view=View(root,p,pid)
        self.views.append(view)

        children=root.getchildren()
        if children is not None:
            for i in children:
                self.for_all(i,root,view.id)
