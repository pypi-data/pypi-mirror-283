from ffre import FileFinder
from stcube._pyqt_pack import UISupport
import files3
import os

VERSION = '0.0.2'

def reinsert_indent(text, keep_raw:bool=False, *, indent:str=None, strip:str=None) -> str:
    """
    Reinsert the indent of each line.
    :param text: str. The text to reinsert the indent.
    :param keep_raw: bool. Keep the raw indent of the each line. / If False, strip each line
    *
    :param indent: str. The indent to reinsert. Default is \t.
    :param strip: str. The characters to strip from the start of each line. Default is " \t".
    :return: str. The text with the indent reinserted.
    """
    if indent is None:
        indent = "\t"
    if strip is None:
        strip = " \t"

    lines = [line for line in text.split("\n") if line]
    if not lines:
        return text

    if not keep_raw:
        lines = [line.lstrip(strip) for line in lines]

    return "\n".join(indent + line for line in lines)

class Functional:
    key = 'undefined'
    doc = None
    sys = ['loading']
    def __init__(self, ce):
        self.ce = ce

    def loading(self):
        """
        This function is called when the functional is loading.
        * Used in child class.
        :return:
        """
        pass

    def __call__(self):
        print("This is System Functionalities. Used for test.")

    def __str__(self):
        _doc = self.doc if self.doc is not None else ''
        return f"{self.__class__.__name__}({self.key}): \n{_doc}"

UISP = UISupport()

class FQuit(Functional):
    key = 'q|quit'
    doc = """
    Quit the STCube command executoh
    r.
    """
    def test(self):
        print("This is the test function.")

    def __call__(self):
        global UISP
        del UISP
        UISP = None
        exit()

class FHelp(Functional):
    key = 'h|help'
    doc = """
    Show the help information.
    """
    def __call__(self):
        print(self.ce.gen_help())

class CommandExecutor:
    SPLITTER = '| '
    def __init__(self):
        self._current:str = None
        self.functionals = {}
        self.add(FQuit, FHelp)

    @property
    def current(self):
        return self._current

    @current.setter
    def current(self, value):
        self._current = value


    @staticmethod
    def split(command: str, spliters) -> list:
        commands = [command]
        for sp in spliters:

            _removes, _appends = [], []

            for command in commands:
                _splits = command.split(sp)

                # strip
                for item in _splits:
                    _striped = item.strip()
                    if _striped:
                        _appends.append(_striped)

                if len(_appends) > 1:
                    _removes.append(command)

            for remove in _removes:
                commands.remove(remove)

            commands.extend(_appends)

        # 移除重复项并且保留顺序
        _commands = []
        for command in commands:
            if command not in _commands:
                _commands.append(command)

        return _commands


    def get(self, key:str|Functional, default=None):
        if issubclass(key, Functional):
            key = key.key
        return self.functionals.get(key, default)

    def add(self, *functionals:Functional):
        for functional in functionals:
            # Functional类的子类，但不能是实例
            if isinstance(functional, type) and issubclass(functional, Functional):
                self.functionals[functional.key] = functional(self)
            else:
                raise TypeError(f"{self.__class__.__name__}.add: Functional must be subclass of Functional. Not {type(functional)}")

    def remove(self, *keys:str):
        for key in keys:
            if key in self.functionals:
                del self.functionals[key]

    def gen_help(self) -> str:
        """
        生成用于在cmd中显示的帮助信息
        :return:
        """
        help_info = ""
        for key, functional in self.functionals.items():
            _doc = functional.doc if functional.doc is not None else 'This functional has no doc.'
            _doc = reinsert_indent(_doc, keep_raw=True, indent="\t")
            help_info += f"\t-{key}: \n{_doc}\n"
        return help_info

    def __call__(self):
        # loading for each functional
        for fal in self.functionals.values():
            fal.loading()

        # expand the functionals
        _functionals = {}
        for key, functional in self.functionals.items():
            keys = self.split(key, self.SPLITTER)
            for _key in keys:
                assert _key not in _functionals, f"{self.__class__.__name__}.execute: Command '{_key}' is already exists."
                _functionals[_key] = functional

        _help = self.gen_help()

        print(
            f"STCube Command Executor v{VERSION}\n{'-'*60}"
        )

        while True:
            if self.current is not None:
                print(f"[{self.current}:]", end=' ')
            acommands = self.split(input(">>> "), spliters='.')
            if not acommands or not acommands[0]:
                continue
            main_key = acommands[0]
            sub_keys = acommands[1:]

            if main_key not in _functionals:
                print(f"Command '{main_key}' not found.")
                print(_help)
                continue

            _functional = _functionals[main_key]
            if sub_keys:
                for i, skey in enumerate(sub_keys):
                    if skey.startswith('__'):
                        print(f"Cannot access the private command '{main_key}.{skey}'.")
                        _functional = None
                        break

                    _sys = getattr(_functional, 'sys', [])
                    if skey in _sys:
                        print(f"Command '{main_key}.{skey}' is system command. Restricted.")
                        _functional = None
                        break
                    _functional = getattr(_functional, skey, None)
                    if _functional is None:
                        _links = ".".join(sub_keys[:i+1])
                        print(f"Command '{main_key}.{_links}' not found.")
                        print(_help)
                        break
                if _functional is None:
                    continue

            _functional()


HOME_DIR = os.path.expanduser("~")
DESKTOP_DIR = os.path.join(HOME_DIR, "Desktop")
HOME_DIR = os.path.join(HOME_DIR, ".stcube")
if not os.path.exists(HOME_DIR):
    os.makedirs(HOME_DIR)
LIBS_DIR = os.path.join(HOME_DIR, "libs")
MODS_DIR = os.path.join(HOME_DIR, "mods")
HOME_F = files3.files(HOME_DIR)

class Setting:
    def __init__(self):
        self.data = {}

        self.load()

    def save(self):
        HOME_F.stcube = self.data

    def load(self):
        if HOME_F.has('setting'):
            self.data = HOME_F.stcube

if __name__ == '__main__':
    ce = CommandExecutor()
    ce()  # start the command executor


