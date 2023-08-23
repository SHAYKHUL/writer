import sys
import subprocess

from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QAction, QFileDialog, QVBoxLayout, QWidget, QLabel, QComboBox, QLineEdit, QPushButton, QStatusBar
from PyQt5.QtGui import QIcon, QTextCharFormat, QColor, QTextDocument, QFont, QSyntaxHighlighter, QTextFormat
from PyQt5.QtCore import Qt, QRegExp

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTextEdit, QPushButton

class OutputWindow(QDialog):
    def __init__(self, output):
        super().__init__()

        self.setWindowTitle("Code Execution Output")
        self.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout()

        self.output_text_edit = QTextEdit(self)
        self.output_text_edit.setReadOnly(True)
        self.output_text_edit.setPlainText(output)
        layout.addWidget(self.output_text_edit)

        close_button = QPushButton("Close", self)
        close_button.clicked.connect(self.accept)
        layout.addWidget(close_button)

        self.setLayout(layout)


class TextEditor(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.text_edit = QTextEdit(self)
        self.text_edit.cursorPositionChanged.connect(self.update_cursor_position)  # Connect cursor position signal
        self.setCentralWidget(self.text_edit)

        open_action = QAction(QIcon.fromTheme('document-open'), 'Open', self)
        open_action.setShortcut('Ctrl+O')
        open_action.triggered.connect(self.open_file)

        save_action = QAction(QIcon.fromTheme('document-save'), 'Save', self)
        save_action.setShortcut('Ctrl+S')
        save_action.triggered.connect(self.save_file)

        undo_action = QAction(QIcon.fromTheme('edit-undo'), 'Undo', self)
        undo_action.setShortcut('Ctrl+Z')
        undo_action.triggered.connect(self.text_edit.undo)

        redo_action = QAction(QIcon.fromTheme('edit-redo'), 'Redo', self)
        redo_action.setShortcut('Ctrl+Shift+Z')
        redo_action.triggered.connect(self.text_edit.redo)
        
        
        run_action = QAction(QIcon.fromTheme('media-playback-start'), 'Run', self)
        run_action.setShortcut('Ctrl+R')
        run_action.triggered.connect(self.run_code)
        
    


        exit_action = QAction(QIcon.fromTheme('application-exit'), 'Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.close)

        bold_action = QAction(QIcon.fromTheme('format-text-bold'), 'Bold', self)
        bold_action.setShortcut('Ctrl+B')
        bold_action.triggered.connect(self.toggle_bold)

        italic_action = QAction(QIcon.fromTheme('format-text-italic'), 'Italic', self)
        italic_action.setShortcut('Ctrl+I')
        italic_action.triggered.connect(self.toggle_italic)
        
        

        self.word_count_label = QLabel(self)
        self.update_word_count()

        self.syntax_highlight_combo = QComboBox(self)
        self.syntax_highlight_combo.addItems(['None', 'Python'])  # Add more languages as needed
        self.syntax_highlight_combo.currentIndexChanged.connect(self.update_syntax_highlight)

        find_label = QLabel('Find:', self)
        self.find_input = QLineEdit(self)
        self.find_input.returnPressed.connect(self.find_text)  # Connect to returnPressed signal
        find_button = QPushButton('Find', self)
        find_button.clicked.connect(self.find_text)

        self.cursor_position_label = QLabel(self)

        self.status_bar = QStatusBar()
        self.status_bar.showMessage('Ready')

        self.format_toolbar = self.addToolBar('Format')
        self.format_toolbar.addAction(bold_action)
        self.format_toolbar.addAction(italic_action)
        self.format_toolbar.addWidget(self.syntax_highlight_combo)

        self.find_toolbar = self.addToolBar('Find')
        self.find_toolbar.addWidget(find_label)
        self.find_toolbar.addWidget(self.find_input)
        self.find_toolbar.addWidget(find_button)

        menubar = self.menuBar()
        file_menu = menubar.addMenu('File')
        file_menu.addAction(open_action)
        file_menu.addAction(save_action)
        file_menu.addAction(exit_action)

        edit_menu = menubar.addMenu('Edit')
        edit_menu.addAction(undo_action)
        edit_menu.addAction(redo_action)
        edit_menu.addAction(run_action)
      



        layout = QVBoxLayout()
        layout.addWidget(self.word_count_label)
        layout.addWidget(self.text_edit)
        
        central_widget = QWidget(self)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.statusBar().addWidget(self.status_bar)
        self.statusBar().addPermanentWidget(self.cursor_position_label)  # Add permanent widget for cursor position

        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Advanced Text Editor')
        self.show()

    def run_code(self):
        code = self.text_edit.toPlainText()

        if code:
            self.status_bar.showMessage("Running code...")

            try:
                result = subprocess.run(["python", "-c", code], capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    output = result.stdout
                else:
                    output = result.stderr

                self.status_bar.showMessage("Code execution complete.")
                self.show_output(output)
            except subprocess.TimeoutExpired:
                self.status_bar.showMessage("Code execution timed out.")
            except Exception as e:
                self.status_bar.showMessage("An error occurred during code execution.")
                print(e)


    def show_output(self, output):
        # Open a new window to display the output
        output_window = OutputWindow(output)
        output_window.exec_()


    def open_file(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, 'Open File', '', 'Text Files (*.txt);;All Files (*)', options=options)
        if file_path:
            with open(file_path, 'r') as file:
                self.text_edit.setPlainText(file.read())

    def save_file(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self, 'Save File', '', 'Text Files (*.txt);;All Files (*)', options=options)
        if file_path:
            with open(file_path, 'w') as file:
                file.write(self.text_edit.toPlainText())

    def toggle_bold(self):
        fmt = QTextCharFormat()
        fmt.setFontWeight(QFont.Bold if self.text_edit.currentCharFormat().fontWeight() == QFont.Normal else QFont.Normal)
        self.text_edit.mergeCurrentCharFormat(fmt)

    def toggle_italic(self):
        fmt = QTextCharFormat()
        fmt.setFontItalic(not self.text_edit.currentCharFormat().fontItalic())
        self.text_edit.mergeCurrentCharFormat(fmt)

    def update_word_count(self):
        text = self.text_edit.toPlainText()
        word_count = len(text.split())
        self.word_count_label.setText(f"Word Count: {word_count}")

    def update_syntax_highlight(self):
        language = self.syntax_highlight_combo.currentText()
        if language == 'Python':
            self.highlight_python_syntax()
        else:
            self.remove_syntax_highlight()

    def highlight_python_syntax(self):
        text = self.text_edit.toPlainText()
        document = QTextDocument()
        font = QFont()
        font.setFamily("Courier New")
        font.setStyleHint(QFont.Monospace)
        font.setPointSize(12)
        document.setDefaultFont(font)
        self.text_edit.setFont(font)

        # Apply basic syntax highlighting for Python
        highlighter = PythonSyntaxHighlighter(self.text_edit.document())
        self.text_edit.setPlainText(text)

    def remove_syntax_highlight(self):
        self.text_edit.setFont(QFont())  # Reset font to default

    def find_text(self):
        text_to_find = self.find_input.text()
        cursor = self.text_edit.textCursor()
        
        if text_to_find:
            # Set the search options and start searching from the current cursor position
            search_options = QTextDocument.FindFlags()
            found_cursor = self.text_edit.document().find(text_to_find, cursor, search_options)
            
            if found_cursor:
                self.text_edit.setTextCursor(found_cursor)
                self.status_bar.showMessage(f"Found '{text_to_find}'")
            else:
                self.status_bar.showMessage(f"'{text_to_find}' not found")


    def update_cursor_position(self):
        cursor = self.text_edit.textCursor()
        line_number = cursor.blockNumber() + 1
        column_number = cursor.columnNumber() + 1
        self.cursor_position_label.setText(f"Line: {line_number}, Column: {column_number}")

class PythonSyntaxHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.highlighting_rules = []
        self.initialize_highlighting_rules()

    def initialize_highlighting_rules(self):
        # Define highlighting rules using QRegExp and QTextCharFormat
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(Qt.darkBlue)
        keywords = ['def', 'class', 'if', 'else', 'while', 'for', 'return']  # Add more keywords

        for keyword in keywords:
            pattern = QRegExp(r'\b' + keyword + r'\b')
            rule = (pattern, keyword_format)
            self.highlighting_rules.append(rule)

    def highlightBlock(self, text):
        for pattern, format in self.highlighting_rules:
            expression = QRegExp(pattern)
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, format)
                index = expression.indexIn(text, index + length)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setAttribute(Qt.AA_EnableHighDpiScaling)
    editor = TextEditor()
    editor.show()
    sys.exit(app.exec_())
