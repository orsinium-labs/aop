# project
import aop


def multiply(context):
    print(context.aspect, context.args, context.kwargs)
    yield
    context.result *= 100


aop.register(
    handler=multiply,
    modules=aop.match(equals='math'),
    targets=aop.match(regexp='(sin|cos)')
)
