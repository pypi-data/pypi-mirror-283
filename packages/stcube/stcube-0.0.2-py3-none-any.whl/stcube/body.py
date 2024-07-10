import os.path

from stcube.core import *
from stcube.library import Library, unzip_folder
from stcube._pyqt_pack import *
import time
import sys



class FNew(Functional):
    key = 'n|new'
    doc = """
    Create a new Project from Library.
    """
    sys = Functional.sys + ['library', 'get_wizard_info']
    def loading(self):
        library = self.ce.get(Library)
        update = self.ce.get(FUpdate)
        if not library:
            raise Exception("\n\nSystem Error: \n\tComponent<Library> not found. ")
        if not update:
            raise Exception("\n\nSystem Error: \n\tComponent<FUpdate> not found. ")
        self.library = library
        self.update = update

    def get_wizard_info(self) -> tuple[str, str, str]:
        """
        UI
        title: 'New Project Wizard'
            'Input project name:'
            [       Edit                        ]
            'Select a directory:'   btn[...]
            [       ReadOnly Edit               ]
            'Select a library:'
            [       Select Edit                 ]  # lib['name'], lib['mcu'], lib['flash'], lib['ram'], lib['time']
            btn['Create']            btn['Cancel']

        :return:
        """
        libs:list[dict] = self.library.libs()
        if not libs:
            print("No library found.")
            return
        lib_names = [f"{lib['name']} ({lib['mcu']}, FLASH={lib['flash']}, RAM={lib['ram']})" for lib in libs]

        _DEFAULT_DIR = DESKTOP_DIR
        _DEFAULT_PNAME = 'untitled'
        if os.path.exists(os.path.join(_DEFAULT_DIR, _DEFAULT_PNAME)):
            i = 1
            while os.path.exists(os.path.join(_DEFAULT_DIR, f"{_DEFAULT_PNAME}{i}")):
                i += 1
            _DEFAULT_PNAME = f"{_DEFAULT_PNAME}{i}"

        # UI
        app = UISP.app
        win = QWidget()
        win.setFixedHeight(440)
        win.setFixedWidth(720)
        win.setWindowTitle('New Project Wizard')
        layout = QVBoxLayout()
        win.setLayout(layout)
        # Input project name
        layout.addWidget(QLabel('Input project name:'))
        pname_edit = QLineEdit()
        pname_edit.setText(_DEFAULT_PNAME)
        pname_edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        def _auto_default_name():
            if not pname_edit.text():
                pname_edit.setText(_DEFAULT_PNAME)
        pname_edit.textChanged.connect(_auto_default_name)
        pname_edit.setStyleSheet('font-size: 20px; color: #242430;')
        layout.addWidget(pname_edit)

        # Select a directory
        hline = QHBoxLayout()
        layout.addLayout(hline)
        hline.addWidget(QLabel('Select a directory:'))
        dir_edit = QLineEdit()
        dir_edit.setText(_DEFAULT_DIR)
        dir_edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        def _auto_default_dir():
            if not dir_edit.text():
                dir_edit.setText(_DEFAULT_DIR)
        dir_edit.textChanged.connect(_auto_default_dir)
        dir_edit.setStyleSheet('font-size: 20px; color: #242430;')
        def select_dir():
            dir = QFileDialog.getExistingDirectory(win, 'Select Project Directory:', DESKTOP_DIR)
            dir_edit.setText(dir)
        btn = QPushButton('...')
        btn.setFixedWidth(80)
        btn.clicked.connect(select_dir)
        hline.addWidget(btn)
        layout.addWidget(dir_edit)

        # Select a library
        layout.addWidget(QLabel('Select a library:'))
        lib_box = QComboBox()
        lib_box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        lib_box.setStyleSheet('font-size: 20px; color: #242430;')
        lib_box.setEditable(True)
        for i, lib_name in enumerate(lib_names):
            lib_box.addItem(lib_name)
            lib_box.setItemData(i, libs[i])
        layout.addWidget(lib_box)
        _change_lock = [False]
        def _on_text_change(*a):
            if _change_lock[0]:
                return
            _change_lock[0] = True
            # search the lib
            _new = []
            _ctxt = lib_box.currentText()
            for i, lib_name in enumerate(lib_names):
                if _ctxt in lib_name:
                    _new.append(libs[i])
            _new_names = [f"{lib['name']} ({lib['mcu']}, FLASH={lib['flash']}, RAM={lib['ram']})" for lib in _new]
            lib_box.clear()

            for i, lib in enumerate(_new):
                lib_box.addItem(lib_name)
                lib_box.setItemData(i, lib)

            if not _new:
                # set red fore
                lib_box.setStyleSheet('color: red; font-size: 20px;')

                _change_lock[0] = False
                return
            lib_box.setStyleSheet('font-size: 20px; color: #242430;')

            if _ctxt not in _new_names:
                lib_box.setStyleSheet('color: #CA884400; font-size: 20px;')


            lib_box.setCurrentText(_ctxt)

            _change_lock[0] = False

        lib_box.editTextChanged.connect(_on_text_change)
        _res = [False, None, None, None]  # Flag, pname, dir, lib

        # Buttons
        def create():
            pname = pname_edit.text()
            dir = dir_edit.text()
            lib_key = lib_box.currentText()
            if not pname or not dir or not lib_key:
                print('Please input all the information.')
                QPop(RbpopWarn('Please input all the information.', 'Not enough inputs:'))
                return
            if not os.path.isdir(dir):
                print('Please select a valid directory.')
                QPop(RbpopWarn('Please select a valid directory.', 'Invalid directory:'))
                return
            # 判断name是否是合法文件夹名
            if not os.path.isdir(os.path.join(dir, pname)):
                # create the project directory
                try:
                    os.makedirs(os.path.join(dir, pname))
                except:
                    print('Please input a valid project name.')
                    QPop(RbpopWarn('Please input a valid project name.', 'Invalid project name:'))
                    return
            else:
                select = QMessageBox.question(win, 'Warning:', f"Project '{pname}' already exists. Do you want to next?", QMessageBox.Yes | QMessageBox.No)
                if select == QMessageBox.No:
                    return
            if lib_key not in lib_names:
                print('Please select a valid library.')
                QPop(RbpopWarn('Please select a valid library.', 'Invalid library:'))
                return
            lib = lib_box.itemData(lib_names.index(lib_key) )
            _res[0] = True
            _res[1] = pname
            _res[2] = dir
            _res[3] = lib
            win.close()
        def cancel():
            _res[0] = True
            win.close()

        space = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addItem(space)
        hline = QHBoxLayout()
        layout.addLayout(hline)
        btn = QPushButton('Create')
        btn.clicked.connect(create)
        btn.setFixedHeight(60)
        hline.addWidget(btn)
        btn = QPushButton('Cancel')
        btn.clicked.connect(cancel)
        btn.setFixedHeight(60)
        hline.addWidget(btn)

        # 绑定快捷键 Enter和Esc
        def keyPressEvent(event):
            if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
                create()
            elif event.key() == Qt.Key_Escape:
                cancel()
        win.keyPressEvent = keyPressEvent

        # 大字体，consolas
        win.setStyleSheet("font-size: 25px; font-family: Consolas; color: #323648; ")
        # Label设为#643232
        for label in win.findChildren(QLabel):
            label.setStyleSheet('color: #645555; font-size: 20px;')
        win.show()

        while not _res[0]:
            app.processEvents()

        return _res[1:]


    def __call__(self):
        print('Please follow the wizard UI to create a new project:')
        pname, pdir, lib_select = self.get_wizard_info()
        if not pname:
            print('User canceled the operation.')
            return
        unzip_dir = os.path.join(pdir, pname)
        # unzip the lib
        lib_path = lib_select['path']
        if not os.path.exists(lib_path):
            print(f"Non-exists library path: '{lib_path}'.")
            return
        print(f"Create project: from '{lib_select['name']}' to '{unzip_dir}', please wait...")
        unzip_folder(lib_path, unzip_dir)
        print(f'Set Current Project: {os.path.join(pdir, pname)}')
        self.ce.current = os.path.join(pdir, pname)
        print(f"Success create project: '{pname}'.")
        self.update()
        # open explore into project dir
        os.system(f'explorer {os.path.join(pdir, pname)}')


class FOpen(Functional):
    key = 'o|cd|open'
    doc = """
    Change the current project directory.
        * will close the current project if has.
    """

    def loading(self):
        update = self.ce.get(FUpdate)
        if not update:
            raise Exception("\n\nSystem Error: \n\tComponent<FUpdate> not found. ")
        self.update = update

    @staticmethod
    def ask_open() -> str:
        # Ask for the directory
        dir = QFileDialog.getExistingDirectory(None, 'Select Project Directory:', DESKTOP_DIR)
        if not dir:
            print('User canceled the operation.')
            return
        if not Library.IsCubeMxProject(dir):
            print(f'Cd/Open stopped due to the previous errores.')
            return
        return dir

    def __call__(self):
        print('Please select the project directory in UI dialog: ')
        dir = self.ask_open()
        if not dir:
            return
        print(f"Set Current Project: {dir}")
        self.ce.current = dir
        self.update()

class FUpdate(Functional):
    key = 'u|up|update'
    doc = """
    Update the current project to create cpp Entrence.
        * won't action if the main.cpp already exists.
    """

    KEY_SETUP_BEGIN = "/* USER CODE BEGIN 2 */"
    KEY_LOOP_BEGIN = "/* USER CODE BEGIN 3 */"
    DECLARE_BEGIN = "/* USER CODE BEGIN EFP */"

    DECLARE_SETUP = "void setup();"
    DECLARE_LOOP = "void loop();"

    NEW_FILE_CONTENT = '// This file wont changed by stcube later.\n'
    NEW_FILE_CONTENT += '#include "main.h"\n\n'
    NEW_FILE_CONTENT += 'void setup()\n{\n'
    NEW_FILE_CONTENT += '}\n\n'
    NEW_FILE_CONTENT += 'void loop()\n{\n'
    NEW_FILE_CONTENT += '}\n\n'

    def find_mainc(self):
        # find the main.c
        ff = FileFinder(self.ce.current)
        fc = list(ff.find('.c', pattern='main'))
        if not fc:
            print('Cannot find the main.c file.')
            return
        return fc[0]

    def find_mainh(self):
        # find the main.h
        ff = FileFinder(self.ce.current)
        fc = list(ff.find('.h', pattern='main'))
        if not fc:
            print('Cannot find the main.h file.')
            return
        return fc[0]

    def find_maincpp(self):
        # find the main.cpp
        ff = FileFinder(self.ce.current)
        fc = list(ff.find('.cpp', pattern='main'))
        if not fc:
            print('Cannot find the main.cpp file.')
            return
        return fc[0]

    def new_maincpp(self, mainc:str, mainh:str):
        src_dir = os.path.dirname(mainc)
        maincpp = os.path.join(src_dir, 'main.cpp')
        if os.path.exists(maincpp):
            print('main.cpp already exists.')
            return
        with open(maincpp, 'w') as f:
            f.write(self.NEW_FILE_CONTENT)
        print(f"Create new main.cpp: '{maincpp}'")

        # add the call in main.c
        with open(mainc, 'r') as f:
            txt = f.read()
        # add the setup() call
        _pos = txt.index(self.KEY_SETUP_BEGIN)
        if _pos == -1:
            print(f"Cannot find the key '{self.KEY_SETUP_BEGIN}' in the main.c.")
            return
        _pos += len(self.KEY_SETUP_BEGIN)
        txt = txt[:_pos] + f'\n\tsetup();\n' + txt[_pos:]
        # add the loop() call
        _pos = txt.index(self.KEY_LOOP_BEGIN)
        if _pos == -1:
            print(f"Cannot find the key '{self.KEY_LOOP_BEGIN}' in the main.c.")
            return
        _pos += len(self.KEY_LOOP_BEGIN)
        txt = txt[:_pos] + f'\n\tloop();\n' + txt[_pos:]
        with open(mainc, 'w') as f:
            f.write(txt)
        print(f"Add the setup() and loop() call in the main.c: '{mainc}'")

        # add the declaration in main.h
        with open(mainh, 'r') as f:
            txt = f.read()
        _pos = txt.index(self.DECLARE_BEGIN)
        if _pos == -1:
            print(f"Cannot find the key '{self.DECLARE_BEGIN}' in the main.h.")
            return
        _pos += len(self.DECLARE_BEGIN)
        txt = txt[:_pos] + f'\n{self.DECLARE_SETUP}\n{self.DECLARE_LOOP}\n' + txt[_pos:]
        with open(mainh, 'w') as f:
            f.write(txt)
        print(f"Add the setup() and loop() declaration in the main.h: '{mainh}'")



    def __call__(self):
        if not self.ce.current:
            print('No current project. Try to open a project ...')
            dir = FOpen.ask_open()
            if not dir:
                return
            self.ce.current = dir

        mainc = self.find_mainc()
        if not mainc:
            return

        mainh = self.find_mainh()
        if not mainh:
            return

        maincpp = self.find_maincpp()
        if not maincpp:
            print('No main.cpp found, create a new one.')
            self.new_maincpp(mainc, mainh)
            print('Update the current project success.')
            return

        print('No need to update the current project.')
