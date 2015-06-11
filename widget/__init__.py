# encoding=utf8

from . import view, viewgroup, exception


def choice_view(tag):
    if tag.name == 'View':
        return view.View
    elif tag.name == 'ViewGroup':
        return viewgroup.ViewGroup
    return None


def create_view(tag):
    cls = choice_view(tag)
    if not cls:
        raise exception.UnknownTagException(tag)
    return cls(tag)
