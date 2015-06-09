# encoding=utf8


from bs4 import BeautifulSoup, element


class UnexpectedObjectException(Exception):
    def __init__(self, t):
        Exception.__init__(self, 'object must be an instance of %s' % str(t))


class View(object):

    nid = 0

    def __init__(self, tag, parent=None, context='null'):
        """
        @tag 一个BeautifulSoup的节点
        @parent 一个ViewGroup对象
        @context Context的对象，可以为None
        """
        if type(tag) != element.Tag:
            raise UnexpectedObjectException(element.Tag)
        elif type(context) != str:
            raise UnexpectedObjectException(str)
        self.tag = tag
        self.parent = parent
        self.context = context
        self.__id__ = None

    def __getid__(self):
        View.nid += 1
        return View.nid

    def id(self):
        if self.__id__ is None:
            self.__id__ = self.__getid__()
        return self.__id__

    def name(self):
        return 'v%s' % self.id()

    def __str__(self):
        s = 'View %s = View(%s);\n' % (self.name(), self.context)
        s += self.attrs_layout()
        return s

    def attrs_layout(self):
        """处理布局相关的属性"""
        if self.parent is None:
            layout_params = 'ViewGroup.LayoutParams'
        else:
            layout_params = self.parent.layout_params()
        width = self.get_layout_params('width')
        height = self.get_layout_params('height')
        layout_params_name = 'layoutParams%s' % self.id()
        s = '%s %s = %s(%s.%s, %s.%s);\n' % (layout_params,
                                             layout_params_name,
                                             layout_params,
                                             layout_params,
                                             width,
                                             layout_params,
                                             height)
        s += '%s.setLayoutParams(%s);\n' % (self.name(), layout_params_name)
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
