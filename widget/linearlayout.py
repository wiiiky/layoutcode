# encoding=utf8


from .viewgroup import ViewGroup


class LinearLayout(ViewGroup):

    nid = 0

    @classmethod
    def class_name(cls):
        return cls.__name__

    def __init__(self, tag, parent=None, context='null'):
        super(LinearLayout, self).__init__(tag, parent, context)

    def layout_params(self):
        return 'LinearLayout.LayoutParams'

    def __str__(self):
        s = '%s %s = new %s(%s);\n' % (self.class_name(), self.name(),
                                       self.class_name(), self.context)
        s += self.attrs_layout()
        s += '\n'
        s += self.foreach_children()
        return s
