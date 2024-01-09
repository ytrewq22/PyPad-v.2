from scr.scripts import FileLoader, CodeHighlighter, CodeAnalyzer

from PySide6.QtWidgets import QPlainTextEdit, QTextEdit
from PySide6.QtGui import QColor, QTextFormat
from PySide6.QtCore import Qt


class CodeEditorArea(QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setStyleSheet(FileLoader.load_style("scr/styles/code_area.css"))
        self.setObjectName("code-area")

        self.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        CodeHighlighter(self)  # set highlighter
        self.__highlight_current_line()

        # connections
        self.cursorPositionChanged.connect(self.__update_current_line)
        self.cursorPositionChanged.connect(self.__highlight_current_line)
        self.textChanged.connect(self.__highlight_current_line())

        # variables
        self.__current_line = 0

    def __highlight_current_line(self):
        extra_selections = []

        if not self.isReadOnly() and self.hasFocus():
            selection = QTextEdit.ExtraSelection()

            selection.format.setBackground(QColor("#303030"))
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()

            extra_selections.append(selection)

        self.setExtraSelections(extra_selections)

    def __update_current_line(self):
        cursor = self.textCursor()
        self.__current_line = cursor.blockNumber()

    def __insert_around_cursor(self, __symbol_1: str, __symbol_2: str) -> None:
        cursor = self.textCursor()
        selected_text = cursor.selectedText()

        cursor.insertText(f"{selected_text}".join([__symbol_1, __symbol_2]))
        cursor.setPosition(cursor.position() - 1)
        self.setTextCursor(cursor)

    def __pass_duplicate_symbol(self, __target: str) -> None | str:
        cursor = self.textCursor()

        if len(self.toPlainText().split("\n")[self.__current_line][cursor.positionInBlock():]) != 0:

            if self.toPlainText().split("\n")[self.__current_line][cursor.positionInBlock()] == __target:
                cursor.setPosition(cursor.position() + 1)
                self.setTextCursor(cursor)

            else:
                return "exception"

        else:
            return "exception"

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_ParenLeft:
            self.__insert_around_cursor("(", ")")

        elif event.key() == Qt.Key.Key_BraceLeft:
            self.__insert_around_cursor("{", "}")

        elif event.key() == Qt.Key.Key_BracketLeft:
            self.__insert_around_cursor("[", "]")

        elif event.key() == Qt.Key.Key_QuoteDbl:
            self.__insert_around_cursor('"', '"')

        elif event.key() == Qt.Key.Key_Apostrophe:
            self.__insert_around_cursor("'", "'")

        elif event.key() == Qt.Key.Key_ParenRight:
            if self.__pass_duplicate_symbol(")") == "exception":
                super().keyPressEvent(event)

        elif event.key() == Qt.Key.Key_BraceRight:
            if self.__pass_duplicate_symbol("}") == "exception":
                super().keyPressEvent(event)

        elif event.key() == Qt.Key.Key_BracketRight:
            if self.__pass_duplicate_symbol("]") == "exception":
                super().keyPressEvent(event)

        elif event.key() == Qt.Key.Key_Tab:
            self.textCursor().insertText("    ")

        elif event.key() == Qt.Key.Key_Return:
            cursor = self.textCursor()
            previous = self.toPlainText().split("\n")[cursor.blockNumber()]

            if previous == "":
                prev = "//"  # it's need for remove exception - list has no index -1

            elif not previous.isspace() and previous.replace(" ", "") != "":
                try:
                    prev = previous[:cursor.positionInBlock()].rstrip()
                    prev[-1]  # checks if there is a character at the end of the line

                except IndexError:
                    prev = "//none"
            else:
                prev = previous

            if prev[-1] == ":" or self.toPlainText().split("\n")[cursor.blockNumber()][:4] == "    ":
                tab_count = (CodeAnalyzer.find_tabs_in_string(previous) +
                             CodeAnalyzer.check_last_character_is_colon(prev))
                cursor.insertText("\n" + ("    " * tab_count))

            else:
                super().keyPressEvent(event)

        else:
            super().keyPressEvent(event)
