from stcube import *
from stcube.body import FNew, FCd, FUpdate, FAuto

ce = CommandExecutor()

ce.add(FNew)
ce.add(FCd)
ce.add(FUpdate)
ce.add(FAuto)
ce.add(Library)
ce.add(Module)

if __name__ == '__main__':
    ce()  # start the command executor
