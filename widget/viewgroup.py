# encoding=utf8


from .view import View
from .__init__ import create_view


class ViewGroup (View):

    nid = 0

    @classmethod
    def class_name(cls):
        return cls.__name__

    def __init__(self, tag, parent=None, context='null'):
        super(ViewGroup, self).__init__(tag, parent, context)

    def layout_params(self):
        return 'ViewGroup.LayoutParams'

    def foreach_children(self):
        s = ''
        for tag in self.tag.findChildren(recursive=False):
            v = create_view(tag, self, self.context)
            s += str(v) + '\n'
        return s

    def __str__(self):
        raise AbstractClass(self.class_name())
