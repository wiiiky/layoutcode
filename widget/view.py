# encoding=utf8


from .base import ViewInterface
from .exception import *


class View (ViewInterface):

    nid = 0

    @classmethod
    def class_name(cls):
        return cls.__name__

    def __init__(self, tag, parent=None, context='null'):
        """
        @tag 一个BeautifulSoup的节点
        @parent 一个ViewGroup对象
        @context Context的对象的名字
        """
        super(View, self).__init__(tag, parent, context)

    def name(self):
        return '%s%s' % (self.class_name().lower(), self.id())

    def attrs_layout(self):
        """处理布局相关的属性"""
        if self.parent is None:
            layout_params = 'ViewGroup.LayoutParams'
        else:
            layout_params = self.parent.layout_params()
        width = self.get_layout_params('width')
        height = self.get_layout_params('height')
        layout_params_name = self.get_layout_params_name()
        s = '%s %s = new %s(%s.%s, %s.%s);\n' % (layout_params,
                                                 layout_params_name,
                                                 layout_params,
                                                 layout_params,
                                                 width,
                                                 layout_params,
                                                 height)
        s += '%s.setLayoutParams(%s);\n' % (self.name(), layout_params_name)
        if self.parent:
            s += '%s.addView(%s);\n' % (self.parent.name(), self.name())
        return s

    def get_layout_params(self, attr):
        """解析android:layout_width和android:layout_height"""
        if attr == 'width':
            attr = 'android:layout_width'
        else:
            attr = 'android:layout_height'
        if attr not in self.tag.attrs:
            return 'WRAP_CONTENT'
        return self.tag.attrs[attr].upper()

    def __str__(self):
        s = 'View %s = new View(%s);\n' % (self.name(), self.context)
        s += self.attrs_layout()
        return s
