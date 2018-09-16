import traceback
from abc import ABC, abstractmethod
from ..helper.traceback_info import TracebackInfo


def run_get_traceback(function_to_run, *args, **kwargs):
    """ Run function and returns TracebackInfo if an exception have been raised
    """
    try:
        return function_to_run(*args, **kwargs)
    except Exception as e:
        return TracebackInfo(e)


class ControllerBase(ABC):
    __manager = None

    def setup(self, manager):
        if manager is None:
            raise AssertionError("manager can't be None")
        self.__manager = manager

    @property
    def manager(self):
        if self.__manager is None:
            raise AssertionError("manager is None, You must call Controller.setup() first")
        return self.__manager

    def start_install(self):
        ret = run_get_traceback(self._start_install)
        if isinstance(ret, TracebackInfo):
            self.display_unhandled_error("install", ret)

    def start_uninstall(self):
        """ Start uninstall
        """
        ret = run_get_traceback(self._start_uninstall)
        if isinstance(ret, TracebackInfo):
            self.display_unhandled_error("uninstall", ret)

    def start_update(self):
        """ Start update"""
        ret = run_get_traceback(self._start_update)
        if isinstance(ret, TracebackInfo):
            self.display_unhandled_error("update", ret)

    @abstractmethod
    def display_unhandled_error(self, stage, traceback_info):
        pass

    @abstractmethod
    def _start_install(self):
        """ Start install
        """
        pass

    @abstractmethod
    def _start_uninstall(self):
        """ Start uninstall
        """
        pass

    @abstractmethod
    def _start_update(self):
        """ Start update"""
        pass
