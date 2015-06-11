# encoding=utf8


from bs4 import element


class ViewGroupInterface (object):

    def __init__(self):
        self.__id__ = None

    def __str__(self):
        return ''

    def __getid__(self):
        return 0

    def id(self):
        if self.__id__ is None:
            self.__id__ = self.__getid__()
        return self.__id__

    def name(self):
        return 'ViewGroupInterface%s' % self.id()

    def layout_params(self):
        return 'ViewGroup.LayoutParams'


class ViewGroup (ViewGroupInterface):

    nid = 0

    def __init__(self, tag, parent=None, context='null'):
        """
        @tag 一个BeautifulSoup的节点
        @parent 一个ViewGroup对象
        @context Context的对象，可以为None
        """
        ViewGroupInterface.__init__(self)
        if type(tag) != element.Tag:
            raise UnexpectedTypeException(element.Tag)
        elif tag.name != 'ViewGroup':
            raise UnexpectedTagException('View', tag.name)
        elif type(context) != str:
            raise UnexpectedTypeException(str)
        self.tag = tag
        self.parent = parent
        self.context = context

    def __str__(self):
        return ''

    def __getid__(self):
        ViewGroup.nid += 1
        return View.nid

    def name(self):
        return 'viewGroup%s' % self.id()
