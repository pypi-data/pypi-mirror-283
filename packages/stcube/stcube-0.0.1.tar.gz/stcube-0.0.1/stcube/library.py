import os.path

from stcube.core import *
from stcube._pyqt_pack import *
from stcube.ioc import STCubeIOC
from stcube.ld import STCubeld
import colorama
import datetime
import zipfile
import shutil


def zip_folder(folder_path, output_path):
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, folder_path))

def unzip_folder(zip_path, output_path):
    with zipfile.ZipFile(zip_path, 'r') as zipf:
        zipf.extractall(output_path)

class Library(Functional):
    key = 'l|lib'
    doc = """
    Library management.
        - Library is made from stm32cube project directory.
        - Need gen codes first in cubemx
    .new: Create a new library from the stm32cube project directory.
    .exp: Open the library directory in the explorer.
    """
    sys = Functional.sys + ['libs', 'is_ioc_dir']
    def loading(self):
        # check LIBS_DIR
        if not os.path.exists(LIBS_DIR):
            os.makedirs(LIBS_DIR)

    def libs(self) -> list[dict]:
        ff = FileFinder(LIBS_DIR)
        fc = ff.find('.zip', '.ZIP', pattern='STCUBE_.*')

        _res = []
        _infos = HOME_F.LIBS_INFO if HOME_F.has('LIBS_INFO') else {}
        for fpath in fc:
            fname = os.path.splitext(os.path.basename(fpath))[0]
            last_change_time = os.path.getmtime(fpath)
            if fname in _infos:
                _info = _infos[fname]
                _res.append({
                    'name': fname,
                    'path': fpath,
                    'mcu': _info['mcu'],
                    'flash': _info['flash'],
                    'ram': _info['ram'],
                    'time': datetime.datetime.fromtimestamp(last_change_time).strftime("%Y-%m-%d %H:%M:%S")
                })
            else:
                _res.append({
                    'name': fname,
                    'path': fpath,
                    'mcu': 'Unknown',
                    'flash': 'Unknown',
                    'ram': 'Unknown',
                    'time': datetime.datetime.fromtimestamp(last_change_time).strftime("%Y-%m-%d %H:%M:%S")
                })
        return _res

    def is_ioc_dir(self, dir):
        """
        Check if the directory is a STM32Cube project directory.
        :param dir:
        :return:
        """
        # Check ioc in it
        _fnames = os.listdir(dir)
        _has_ioc = any([fname.endswith('.ioc') for fname in _fnames])
        if not _has_ioc:
            print(f"Can not find the .ioc file in the directory '{dir}'.")
            QPop(RbpopError, "'New' Failed:", "Can not find the .ioc file in the directory.")
        # Check .mxproject .project .cproject in it
        _has_flash_ld = any([fname.upper().endswith("_FLASH.LD") for fname in _fnames])
        if not _has_flash_ld:
            print(f"Can not find the *_FLASH.ld file in the directory '{dir}'.")
            print(f"Please save & gen codes in STM32CubeMX first.")
            QPop(RbpopError, "'New' Failed:", "Can not find the *_FLASH.ld file in the directory.")
        # check Core directory
        _core_dir = os.path.join(dir, 'Core')
        if not os.path.exists(_core_dir):
            print(f"Can not find the 'Core' directory in the directory '{dir}'.")
            print(f"Please save & gen codes in STM32CubeMX first.")
            QPop(RbpopError, "'New' Failed:", "Can not find the 'Core' directory in the directory.")

        return _has_ioc and _has_flash_ld and os.path.exists(_core_dir)

    def new(self):
        # Select stm32cube project directory
        # always at front
        print("Please select the STM32Cube project directory. In the dialog:")

        dir = QFileDialog.getExistingDirectory(None, 'Select STM32Cube Project Directory', DESKTOP_DIR,
                                               QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)

        if not dir:
            print("User canceled the operation.")
            return

        if not self.is_ioc_dir(dir):
            print(f'New lib stopped due to the previous errores.')
            return

        print(
            colorama.Fore.GREEN +
            f"selecte: '{dir}'."
            + colorama.Style.RESET_ALL
        )

        # get the last directory name
        _dir = os.path.basename(dir)

        # check if the lib is already exists
        _tar_path = os.path.join(LIBS_DIR, f'STCUBE_{_dir}.zip')
        if os.path.exists(_tar_path):
            print(f"Library 'STCUBE_{_dir}' is already exists. Will move old into 'backups'.")

            # create backup dir
            _backup_dir = os.path.join(LIBS_DIR, 'backups')
            if not os.path.exists(_backup_dir):
                os.makedirs(_backup_dir)

            # backup the old lib
            last_change_time = os.path.getmtime(_tar_path)
            _backup_path = os.path.join(_backup_dir, f'STCUBE_{_dir}_backup_before_{datetime.datetime.fromtimestamp(last_change_time).strftime("%Y-%m-%d_%H-%M-%S")}.zip')
            shutil.move(_tar_path, _backup_path)

        # NOTE: Add info and save.

        # find ioc
        ff = FileFinder(dir)
        fc = list(ff.find('.ioc', pattern='.*'))
        if len(fc) > 1:
            print(
                colorama.Fore.YELLOW +
                f"Find {len(fc)} .ioc files in the directory '{dir}'. Will use the first '{os.path.basename(fc[0])}'."
                + colorama.Style.RESET_ALL
            )
        ioc = STCubeIOC(fc[0])
        # find ld
        fc = list(ff.find('.ld', pattern='.*_[fF][lL][aA][sS][hH]'))
        if len(fc) > 1:
            print(
                colorama.Fore.YELLOW +
                f"Find {len(fc)}_FLASH.ld files in the directory '{dir}'. Will use the first '{os.path.basename(fc[0])}'."
                + colorama.Style.RESET_ALL
            )
        ld = STCubeld(fc[0])

        mcu_name = ioc.mcu_name
        flash = f"{ld.flash // 1000}K"
        ram = f"{ld.ram // 1000}K"

        if not HOME_F.has('LIBS_INFO'):
            HOME_F.LIBS_INFO = {}
        _infos:dict = HOME_F.LIBS_INFO
        _infos[f'STCUBE_{_dir}'] = {
            'mcu': mcu_name,
            'flash': flash,
            'ram': ram
        }
        HOME_F.LIBS_INFO = _infos

        # zip the project directory
        print(f"Creating library 'STCUBE_{_dir}'<MCU:{mcu_name}, FLASH:{flash}, RAM:{ram}> from the directory '{dir}', please wait...")
        zip_folder(dir, _tar_path)
        print(f"Library 'STCUBE_{_dir}' is created.")

    def exp(self):
        """
        open liv dir in explore
        :return:
        """
        os.system(f'explorer {LIBS_DIR}')

    def __call__(self):
        """
        list libs
        :return:
        """
        _libs = self.libs()
        if _libs:
            print(colorama.Fore.BLUE + f"STCube Libraries:{colorama.Fore.RESET}\nLib Name\tMCU Type\tFlash\tRAM\tChange Time\n{'-'*60}")
            for lib in _libs:
                print(f"{lib['name'][:30]}\t{lib['mcu']}\t{lib['flash']}\t{lib['ram']}\t{lib['time']}")
        else:
            print(f"No libraries found.")
