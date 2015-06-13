# encoding=utf8

from bs4 import element
from .exception import *


class ViewInterface (object):

    nid = 0
    lpid = 0

    @classmethod
    def class_name(cls):
        return cls.__name__

    def __init__(self, tag, parent=None, context='null'):
        """
        @tag 一个BeautifulSoup的节点
        @parent 一个ViewGroup对象
        @context Context的对象的名字
        """
        self.__id__ = None
        self.__lpid__ = None
        if type(tag) != element.Tag:
            raise UnexpectedTypeException(element.Tag)
        elif tag.name != self.class_name():
            raise UnexpectedTagException(self.class_name(), tag.name)
        elif type(context) != str:
            raise UnexpectedTypeException(str)
        self.tag = tag
        self.parent = parent
        self.context = context

    def __str__(self):
        return ''

    def __getid__(self):
        cls = type(self)
        cls.nid += 1
        return cls.nid

    def __getlpid__(self):
        cls = ViewInterface
        cls.lpid += 1
        return cls.lpid

    def get_layout_params_name(self):
        if self.__lpid__ is None:
            self.__lpid__ = self.__getlpid__()
        return 'layoutParams%s' % self.__lpid__

    def id(self):
        if self.__id__ is None:
            self.__id__ = self.__getid__()
        return self.__id__

    def attrs_layout(self):
        return ''

    def get_layout_params(self, attr):
        return ''
