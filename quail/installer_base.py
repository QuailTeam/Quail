import os
import pathlib
import shutil
from . import helper
from .constants import Constants


class InstallerBase:

    def __init__(self,
                 name,
                 binary,
                 icon,
                 solution,
                 publisher='Quail',
                 console=False,
                 integrity=False):
        self._name = name
        self._binary = binary
        self._icon = icon
        self._solution = solution
        self._publisher = publisher
        self._console = console
        self._install_path = self.build_install_path()
        self._integrity = integrity

    @property
    def solution(self):
        return self._solution

    @property
    def name(self):
        return self._name

    @property
    def icon(self):
        return self._icon

    @property
    def binary(self):
        return self._binary

    @property
    def publisher(self):
        return self._publisher

    @property
    def console(self):
        return self._console

    def build_install_path(self):
        '''Build install path
        This function can be overriden to install files to somewhere else
        '''
        return os.path.join(str(pathlib.Path.home()), '.quail', self.name)

    def get_install_path(self, *args):
        '''Get file from install path'''
        return os.path.join(self._install_path, *args)

    def _verify_integrity(self):
        verifier = helper.IntegrityVerifier(self.get_install_path())
        bad_files = verifier.verify()
        if len(bad_files):
            raise AssertionError("Corrupt files: " + str(bad_files))

    def install(self):
        if not self.solution.open():
            raise AssertionError("Can't access solution")
        if os.path.exists(self.get_install_path()):
            shutil.rmtree(self.get_install_path())
        os.makedirs(self.get_install_path(), 0o777, True)
        for root, dirs, files in self.solution.walk():
            for sdir in dirs:
                os.makedirs(self.get_install_path(root, sdir), 0o777, True)
            for sfile in files:
                shutil.copy2(self.solution.get_file(os.path.join(root, sfile)),
                             self.get_install_path(root))
        self.solution.close()
        shutil.copy2(helper.get_script(), self.get_install_path())
        if helper.running_from_script():
            shutil.copytree(helper.get_module_path(),
                            os.path.join(self.get_install_path(), "quail"))
        if self._integrity:
            self._verify_integrity()

    def uninstall(self):
        shutil.rmtree(self.get_install_path())

    def is_installed(self):
        return os.path.exists(self.get_install_path())
