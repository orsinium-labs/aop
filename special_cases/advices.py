# project
import advice


def multiply(context):
    print(context.aspect, context.args, context.kwargs)
    yield
    context.result *= 100


advice.register(
    handler=multiply,
    modules=advice.match(equals='math'),
    targets=advice.match(regexp='(sin|cos)')
)
