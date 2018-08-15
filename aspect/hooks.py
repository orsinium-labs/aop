from .module import AspectModule


class AspectLoader():
    def create_module(self, spec):
        module = super().create_module(spec)
        new_module = AspectModule(module.__name__)
        AspectModule.__dict__.update(module.__dict__)
        return new_module
