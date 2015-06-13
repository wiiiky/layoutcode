# encoding=utf8


def choice_view(tag):
    from .view import View
    from .linearlayout import LinearLayout
    views = [View, LinearLayout]
    for cls in views:
        if tag.name == cls.class_name():
            return cls
    return None


def create_view(tag, parent=None, context='null'):
    from .exception import UnknownTagException
    cls = choice_view(tag)
    if not cls:
        raise UnknownTagException(tag)
    return cls(tag, parent, context)
