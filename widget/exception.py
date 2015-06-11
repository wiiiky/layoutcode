# encoding=utf8


class UnexpectedTypeException (Exception):
    def __init__(self, t, _t):
        msg = 'unexpected type %s, must be %s' % (str(_t), str(t))
        Exception.__init__(self, msg)


class UnexpectedTagException (Exception):
    def __init__(self, name, _name):
        msg = 'unexpected tag name %s, must be %s' % (_name, name)
        Exception.__init__(self, msg)


class UnknownTagException(Exception):
    def __init__(self, tag):
        msg = '%s is unknown' % str(tag.name)
        Exception.__init__(self, msg)
