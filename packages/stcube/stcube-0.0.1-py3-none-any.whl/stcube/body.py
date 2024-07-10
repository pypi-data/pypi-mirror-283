from stcube.core import *

class FNew(Functional):
    key = 'n|new'
    doc = """
    Create a new Project from Library.
    """

    def __call__(self):
        print("In FNew.__call__")

class FCd(Functional):
    key = 'o|cd|open'
    doc = """
    Change the current project directory.
        * will close the current project if has.
    """

    def __call__(self):
        print("In FCd.__call__")

class FUpdate(Functional):
    key = 'u|up|update'
    doc = """
    Update the current project to maintaince it's entry.
    """

    def __call__(self):
        print("In FUpdate.__call__")

class FAuto(Functional):
    key = 'a|auto'
    doc = """
    Auto update when cubemx saving. 
        * check the file change time.
    """

    def __call__(self):
        print("In FAuto.__call__")