from stcube.core import CommandExecutor
from stcube.modules import Module
from stcube.library import Library
from stcube.body import FNew, FOpen, FUpdate

def cmd_entry():
    ce = CommandExecutor()

    ce.add(Library)
    ce.add(Module)
    ce.add(FNew)
    ce.add(FOpen)
    ce.add(FUpdate)

    ce()  # start the command executor


if __name__ == '__main__':
    cmd_entry()
