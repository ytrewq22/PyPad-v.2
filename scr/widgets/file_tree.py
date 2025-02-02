from scr.scripts import FileLoader, IconProvider
from scr.exceptions import NotDirectoryError

import os

from PySide6.QtWidgets import QTreeView, QFileSystemModel, QAbstractItemView


class FileTree(QTreeView):
    def __init__(self) -> None:
        super().__init__()

        self.setStyleSheet(FileLoader.load_style("scr/styles/file_tree.css"))
        self.setObjectName("file-tree")
        self.setMinimumWidth(300)

        self.setAcceptDrops(True)
        self.setDragEnabled(True)
        self.setDragDropMode(QAbstractItemView.DragDropMode.InternalMove)
        self.setIndentation(20)
        self.setSelectionBehavior(QTreeView.SelectionBehavior.SelectRows)
        self.setEditTriggers(QTreeView.EditTrigger.NoEditTriggers)

        self.model = QFileSystemModel()
        self.model.setRootPath(os.getcwd())
        self.setModel(self.model)
        self.setRootIndex(self.model.index(os.getcwd()))
        self.setHeaderHidden(True)
        self.model.setIconProvider(IconProvider())

        for i in range(1, 4):
            self.header().setSectionHidden(i, True)

    def get_path_by_index(self, __index) -> str:
        return self.model.filePath(__index)

    def get_file_icon(self, __index):
        return self.model.fileIcon(__index)

    def set_project_dir(self, __path: str):
        if not os.path.isdir(__path):
            raise NotDirectoryError("This must be a directory not file")

        self.model.setRootPath(__path)
        self.setRootIndex(self.model.index(__path))

    def open_file(self, __path: str) -> None:
        self.open_directory(os.path.dirname(__path))

    def open_directory(self, __path: str) -> None:
        self.model.setRootPath(__path)
        self.setRootIndex(self.model.index(__path))

    def show_hide_file_tree(self) -> None:
        if self.isVisible():
            self.setVisible(False)
        else:
            self.setVisible(True)
