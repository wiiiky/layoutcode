# encoding=utf8


class UnexpectedTypeException (Exception):
    def __init__(self, t, _t):
        msg = 'unexpected type %s, must be %s' % (str(_t), str(t))
        super(UnexpectedTypeException, self).__init__(msg)


class UnexpectedTagException (Exception):
    def __init__(self, name, _name):
        msg = 'unexpected tag name %s, must be %s' % (_name, name)
        super(UnexpectedTagException, self).__init__(msg)


class UnknownTagException(Exception):
    def __init__(self, tag):
        msg = '%s is unknown' % str(tag.name)
        super(UnknownTagException, self).__init__(msg)


class AbstractClass(Exception):
    def __init__(self, cls):
        msg = '% is an abstract class, cannot be instantiated!!!'
        super(AbstractClass, self).__init__(msg)
