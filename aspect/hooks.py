from .module import wrap_module


class AspectLoader():
    def create_module(self, spec):
        module = super().create_module(spec)
        return wrap_module(module)
