from stcube.core import *
from stcube._pyqt_pack import *

class Module(Functional):
    key = 'm|mod'
    doc = """
    Modules management.
        - Module is made from some .c/cpp .h/hpp files.
        - Import module will copy file and write the main.h
    .new: Create a new module from current project directory.
    .exp: Open the module directory in the explorer.
    """
    sys = Functional.sys + ['mods']
