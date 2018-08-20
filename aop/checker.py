# project
from .aspect import Aspect
from .joinpoint import JoinPoint
from .module import AspectModule


def patched(obj):
    return isinstance(obj, (Aspect, JoinPoint, AspectModule))
