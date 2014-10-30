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

        layout_weight=None
        layout_width=None
        layout_height=None
        
        id=None
        var=None
        #第一次遍历，先提取出id，以及layout_width、layout_height、layout_weight
        for k,v in e.items():
            key=self.handle_key(k)
            value=self.handle_value(v)
            if key=="id":
                id=self.get_id(value)
            elif key=="layout_width":
                layout_width=self.convert_layout(value)
            elif key=="layout_height":
                layout_height=self.convert_layout(value)
            elif key=="layout_weight":
                layout_weight=value

        if id is None:
            var=get_tmp_name()
        else:
            var=id

        ignored=["id","context","layout_width","layout_height","layout_weight"]    # 忽略的属性

        params=None
        margins=var + "Margins"

        code=[]
        code.append(self_type + " "+ var + " = new " + self_type + "(this);")

        if id:
            code.append(var + ".setId(R.id." + id + ");")

        if parent_id:
            code.append(parent_id + ".addView(" + var +");")


        if layout_width or layout_height or layout_weight:
            params=var + "Params"
            if parent_id:
                code.append(parent_type + ".LayoutParams " + params + " = (" + parent_type + ".LayoutParams)" + var + ".getLayoutParams();")
                if layout_width:
                    code.append(params + ".width=" + layout_width + ";")
                if layout_height:
                    code.append(params + ".height=" + layout_height + ";")
                if layout_weight:
                    code.append(params + ".weight=" + layout_weight + ";")
            else:
                width = layout_width or "0"
                height = layout_height or "0"
                code.append("ViewGroup.LayoutParams "+params+"=new ViewGroup.LayoutParams("+width+", "+height+");")
                code.append(var+".setLayoutParams("+params+");")
        else:
            #print("layout_weight and layout_height are neither specified")
            params=var + "Params"
            code.append(parent_type + ".LayoutParams " + params + " = (" + parent_type + ".LayoutParams)" + var + ".getLayoutParams();")


        #第二次遍历,margin和padding需要统一处理
        margin_left=None
        margin_right=None
        margin_top=None
        margin_bottom=None
        
        paddingLeft=None
        paddingRight=None
        paddingTop=None
        paddingBottom=None
        paddingStart=None
        paddingEnd=None

        for k,v in e.items():
            key=self.handle_key(k)
            value=self.handle_value(v)
            if key=="layout_marginleft":
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
            elif key=="layout_below":
                belowid=self.convert_id(value)
                code.append(params + ".addRule(" + parent_type + ".BELOW,"+belowid+");")
            elif key=="gravity":
                gravity=self.convert_gravity(value)
                code.append(var + ".setGravity(" + gravity + ");" )
            elif key=="layout_alignparentleft":
                if value=="true":
                    code.append(params + ".addRule(" + parent_type + ".ALIGN_PARENT_LEFT);")
                else:
                    code.append(params + ".removeRule(" + parent_type + ".ALIGN_PARENT_LEFT);")
            elif key=="layout_alignparentright":
                if value=="true":
                    code.append(params + ".addRule(" + parent_type + ".ALIGN_PARENT_RIGHT);")
                else:
                    code.append(params + ".removeRule(" + parent_type + ".ALIGN_PARENT_RIGHT);")
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
            elif key=="src":  
                src=self.convert_src(value)
                code.append(var + ".setImageDrawable(" + src + ");")
            elif key=="background":
                bg=self.convert_background(value)
                code.append(var + ".setBackgroundResource(" + bg + ");")
            elif key=="style":  # not supported
                pass
                #style=self.convert_style(value)
                #code.append(self.get_style_code(self_type,var,style))
            elif key=="completionthreshold":
                code.append(var + ".setThreshold(" + value + ");")
            elif key=="inputtype":
                inputtype=self.convert_inputtype(value)
                code.append(var + ".setInputType(" + inputtype + ");")
            elif key=="nextfocusdown":
                nextid=self.convert_id(value)
                code.append(var + ".setNextFocusDownId(" + nextid + ");")
            elif key=="imeoptions":
                opt=self.convert_imeoption(value)
                code.append(var + ".setImeOptions(" + opt + ");")
            elif key=="typeface":
                face=self.convert_typeface(value)
                code.append(var + ".setTypeface(" + face + ");")
            elif key=="ems":
                code.append(var + ".setEms(" + value + ");")
            elif not list_contains(ignored,key):
                print("unkonwn : " +key + "|" + value)

        if paddingLeft or paddingRight or paddingTop or paddingBottom:
            left="0"
            right="0"
            top="0"
            bottom="0"
            if paddingLeft:
                left="(int)("+paddingLeft+"*getResources().getDisplayMetrics().density)"
            if paddingRight:
                right="(int)("+paddingRight+"*getResources().getDisplayMetrics().density)"
            if paddingTop:
                top="(int)("+paddingTop+"*getResources().getDisplayMetrics().density)"
            if paddingBottom:
                bottom="(int)("+paddingBottom+"*getResources().getDisplayMetrics().density)"
            code.append(var + ".setPadding("+left+","+top+","+right+","+bottom+");")
        elif paddingStart or paddingEnd or paddingTop or paddingBottom:
            start="0"
            end="0"
            top="0"
            bottom="0"
            if paddingStart:
                start="(int)("+paddingStart+"*getResources().getDisplayMetrics().density)"
            if paddingEnd:
                end="(int)("+paddingEnd+"*getResources().getDisplayMetrics().density)"
            if paddingTop:
                top="(int)("+paddingTop+"*getResources().getDisplayMetrics().density)"
            if paddingBottom:
                bottom="(int)("+paddingBottom+"*getResources().getDisplayMetrics().density)"
            code.append(var + ".setPaddingRelative("+start+","+top+","+end+","+bottom+");")
                
        if margin_left or margin_right or margin_top or margin_bottom:
            left="0"
            top="0"
            right="0"
            bottom="0"
            if margin_left:
                left="(int)("+margin_left+"*getResources().getDisplayMetrics().density)"
            if margin_top:
                top="(int)("+margin_top+"*getResources().getDisplayMetrics().density)"
            if margin_right:
                right="(int)("+margin_right+"*getResources().getDisplayMetrics().density)"
            if margin_bottom:
                bottom="(int)("+margin_bottom+"*getResources().getDisplayMetrics().density)"
            code.append(params + ".setMargins("+left+","+top+","+right+","+bottom+");")

        self.id=var
        self.code=code

    def get_id(self,v):
        i=v.find("/")
        if i>0:
            return v[i+1:]
        return v

    def convert_id(self,v):
        i=v.find("/")
        if i>0:
            return "R.id." + v[i+1:]
        print("unknown value:",v)
        return "unknown"

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
        print("unknown value :",v)
        return "unknown";

    def convert_background(self,v):
        i=v.find("drawable/")
        if i>=0:
            return "R.drawable." + v[i+9:]
        i=v.find("color/")
        if i>=0:
            return "R.color." + v[i+6:]
        print("unknown value :",v)
        return "unknown"

    def convert_style(self,v):
        i=v.find("style/")
        if i>=0:
            return "R.style." + v[i+6:]
        print("unknown value :",v)
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
        print("unknown value :",v)
        return "unknown"

    def convert_inputtype(self,v):
        if v=="textPassword":
            return "InputType.TYPE_CLASS_TEXT|InputType.TYPE_TEXT_VARIATION_PASSWORD"
        elif v=="textVisiblePassword":
            return "InputType.TYPE_CLASS_TEXT|InputType.TYPE_TEXT_VARIATION_VISIBLE_PASSWORD"
        elif v=="textEmailAddress":
            return "InputType.TYPE_CLASS_TEXT|InputType.TYPE_TEXT_VARIATION_EMAIL_ADDRESS"
        print("unknown value :",v)
        return "unknown"

    def convert_typeface(self,v):
        if v=="monospace":
            return "Typeface.MONOSPACE"
        elif v=="sans":
            return "Typeface.SANS_SERIF"
        elif v=="serif":
            return "Typeface.SERIF"

        return "Typeface.create(\"" + v + "\",Typeface.NORMAL)"

    def convert_dp(self,v):
        if v.endswith("dp"):
            return str(int(v[:-2]))
        i=v.find("dimen/")
        if i>=0:
            return "getResources().getDimension(R.dimen."+ v[i+6:] +")"
        return "0"

    def convert_imeoption(self,v):
        if v=="actionNext":
            return "IME_ACTION_NEXT"
        elif v=="actionDone":
            return "IME_ACTION_DONE"
        elif v=="actionGo":
            return "IME_ACTION_GO"
        print("unknown value:",v)
        return "unknown"

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
        print("unknown value :",v)
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
            var="res"
            all=all.replace("getResources()",var)
            new="Resources " +var + " = getResources();\n"

            j=all.find("res.getDisplayMetrics().density")
            if j>=0:
                var="density"
                all=all.replace("res.getDisplayMetrics().density",var)
                density="float " +var +" = res.getDisplayMetrics().density;\n"
                new = new + density
            new = new + "\n"
            all=new + all

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
