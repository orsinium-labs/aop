import sys


class ObjectInfo:
    def __init__(self, obj):
        self.klass = getattr(obj, '__class__', obj)
        self.name = getattr(obj, '__name__', self.klass.__name__)
        self.module_name = getattr(obj, '__module__', self.klass.__module__)

    @property
    def module_path(self):
        module = sys.modules.get(self.module_name)
        if not module:
            return ''
        spec = getattr(module, '__spec__', None)
        if not spec:
            return ''
        return spec.origin or ''
