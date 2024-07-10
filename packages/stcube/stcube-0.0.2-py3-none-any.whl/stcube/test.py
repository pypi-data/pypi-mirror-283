from stcube.core import CommandExecutor
from stcube.modules import Module
from stcube.library import Library
from stcube.body import FNew, FOpen, FUpdate

ce = CommandExecutor()

ce.add(Library)
ce.add(Module)
ce.add(FNew)
ce.add(FOpen)
ce.add(FUpdate)

if __name__ == '__main__':
    ce()  # start the command executor
