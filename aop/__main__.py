import sys
import os
import os.path

from .interface import enable


def main():
    # enable import patching
    enable()
    # rewrite command line args
    sys.argv[:] = sys.argv[1:]
    # patch paths
    path = os.path.abspath(sys.argv[0])
    dirpath = os.path.dirname(path)
    sys.path.insert(0, dirpath)
    os.chdir(dirpath)

    # execute module
    with open(path, 'rb') as stream:
        code = compile(stream.read(), path, 'exec')
    globs = {
        '__file__': path,
        '__name__': '__main__',
        '__package__': None,
        '__cached__': None,
    }
    return exec(code, globs)


sys.exit(main())
