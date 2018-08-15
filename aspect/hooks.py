

class AspectLoader():
    def create_module(self, spec):
        module = super().create_module(spec)
        ...
        return module

    def exec_module(self, module):
        super().exec_module(module)
        ...
