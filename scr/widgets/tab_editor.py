from scr.scripts import FileLoader
from scr.data import IconPaths
from .welcome_screen import WelcomeScreen

from PySide6.QtWidgets import QTabWidget
from PySide6.QtGui import QIcon
from PySide6.QtCore import QSize

from typing import Any


class TabEditor(QTabWidget):
    def __init__(self) -> None:
        super().__init__()

        self.setStyleSheet(FileLoader.load_style("scr/styles/tab_editor.css"))
        self.setObjectName("tab-editor")
        self.setMinimumSize(1040, 480)

        self.setTabsClosable(True)
        self.setMovable(True)
        self.setMouseTracking(True)
        self.setIconSize(QSize(20, 20))
        self.tabCloseRequested.connect(self.removeTab)

    def find_by_path(self, __path: str):
        for i in range(self.count()):

            if hasattr(self.widget(i), "get_full_path"):
                if self.widget(i).get_full_path() == __path:
                    return self.widget(i)

    def get_all_tabs(self) -> list:
        return [self.widget(i) for i in range(self.count())]

    def get_all_paths(self):
        res = []

        for i in range(self.count()):

            if hasattr(self.widget(i), "get_full_path"):
                res.append(self.widget(i).get_full_path())

        return res

    def get_current_path(self) -> str:
        if hasattr(self.currentWidget(), "get_full_path"):
            return self.currentWidget().get_full_path()
        else:
            return ""  # it's need for remove exception

    def removeTab(self, __index):
        super().removeTab(__index)

        if self.count() == 0:
            self.addTab(WelcomeScreen(), "Welcome!", IconPaths.SystemIcons.WELCOME)

    def addTab(self, widget: Any, arg__2, icon=None):
        if hasattr(widget, "get_full_path"):
            path = widget.get_full_path()

            if path not in self.get_all_paths():
                super().addTab(widget, arg__2)
            else:
                self.setCurrentWidget(self.find_by_path(path))
        else:
            super().addTab(widget, arg__2)

        if icon != None:
            self.setTabIcon(self.indexOf(widget), QIcon(icon))
