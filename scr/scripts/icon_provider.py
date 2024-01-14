from PySide6.QtGui import QIcon, QAbstractFileIconProvider
from PySide6.QtCore import QFileInfo

from scr.data import IconPaths


class IconProvider(QAbstractFileIconProvider):
    def icon(self, __info: QFileInfo):
        try:

            if __info.isDir():
                return QIcon(IconPaths.FolderIcons.DEFAULT)

            elif __info.isFile():
                if __info.suffix().lower() == "py":
                    return QIcon(IconPaths.FileIcons.PYTHON)
                elif __info.suffix().lower() in ("png", "jpg", "jpeg"):
                    return QIcon(IconPaths.FileIcons.PICTURE)
                elif __info.suffix().lower() in ("qss", "css"):
                    return QIcon(IconPaths.FileIcons.CSS)
                elif __info.suffix().lower() == "json":
                    return QIcon(IconPaths.FileIcons.JSON)
                elif __info.suffix().lower() in ("txt", "md"):
                    return QIcon(IconPaths.FileIcons.TXT)

        except AttributeError:
            pass

        return super().icon(__info)
