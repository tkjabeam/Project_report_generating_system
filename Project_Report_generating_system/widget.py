from PySide6.QtWidgets import (
    QApplication, QTextEdit,
    QStatusBar, QMainWindow, 
    QFileDialog, QFontDialog,
    QTabWidget, QInputDialog,
    QTextBrowser, QVBoxLayout, QDialog
    
    
)

from PySide6.QtGui import QAction, QIcon,QFont,QTextCursor, QTextDocument,QTextCharFormat, QTextImageFormat, QPixmap
from PySide6.QtPrintSupport import QPrinter, QPrintDialog, QPageSetupDialog
from PySide6.QtCore import QDateTime
import sys
import os

basedir = os.path.dirname(__file__)




class PreviewDialog(QDialog):
    def __init__(self, document):
        super().__init__()
        self.setWindowTitle("Report Preview")

        preview_content = QTextBrowser(self)
        preview_content.setDocument(document)  # Set the QTextDocument
        layout = QVBoxLayout(self)
        layout.addWidget(preview_content)
        self.setLayout(layout)


class Mainwindow(QMainWindow):
    windows = []

    def __init__(self):
        super().__init__()
       
        self.text_edit = QTextEdit()
        self.text_edit.setFont(QFont("Arial", 24))
        self.current_report = self.text_edit  # Store the current report 
        self.new_tab()
        self.setWindowTitle("Jason's Window")

                
    def new_tab(self):
        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)
        self.addNewTab()

       

        status_bar = QStatusBar(self)
        self.setStatusBar(status_bar)

        my_icon = QIcon("Project_Notepad/favicon.png")
        self.setWindowIcon(my_icon)

        self.createMenus()
        

    def createMenus(self):

        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu("File")
        new_tab_action = QAction("New tab", self)
        file_menu.addAction(new_tab_action)
        new_tab_action.setStatusTip("create a new tab")
        new_tab_action.triggered.connect(self.addNewTab)

        new_window_action = QAction("New window",self)
        file_menu.addAction(new_window_action)
        new_window_action.setStatusTip("create a new window")
        new_window_action.triggered.connect(self.addNewWindow)

        open_report_action = QAction("Open Report", self)
        open_report_action.triggered.connect(self.open_report)
        file_menu.addAction(open_report_action)

        save_action = QAction("Save report",self)
        file_menu.addAction(save_action)
        save_action.setShortcut("Ctrl+S")  
        save_action.setStatusTip("Save the current tab's content")
        save_action.triggered.connect(self.save_text)

        save_as_action = QAction("Save report as",self)
        file_menu.addAction(save_as_action)
        save_as_action.setShortcut("Ctrl+Shift+S")  # Optional keyboard shortcut
        save_as_action.setStatusTip("Save the current tab's content as a new file")
        save_as_action.triggered.connect(self.save_text_as)

        
        save_all_action = QAction("Save All", self)
        save_all_action.setShortcut("Ctrl+Shift+S")  
        save_all_action.setStatusTip("Save all open tabs")
        save_all_action.triggered.connect(self.save_all_tabs)
        file_menu.addAction(save_all_action)

        convert_to_pdf_action = QAction("Convert to PDF", self)
        convert_to_pdf_action.setShortcut("Ctrl+Shift+P")
        convert_to_pdf_action.setStatusTip("Convert the current tab to PDF")
        convert_to_pdf_action.triggered.connect(self.convert_to_pdf)
        file_menu.addAction(convert_to_pdf_action)


        page_setup_action = QAction("Page Setup", self)
        page_setup_action.setStatusTip("Page setup")
        page_setup_action.triggered.connect(self.page_setup)
        file_menu.addAction(page_setup_action)

        print_action = QAction("Print", self)
        print_action.setShortcut("Ctrl+P")  
        print_action.setStatusTip("Print current tab")
        print_action.triggered.connect(self.print_tab)
        file_menu.addAction(print_action)

        close_tab_action = QAction("Close Tab", self)
        close_tab_action.setShortcut("Ctrl+W")  
        close_tab_action.setStatusTip("Close the current tab")
        close_tab_action.triggered.connect(self.close_current_tab)
        file_menu.addAction(close_tab_action)

        close_window_action = QAction("Close Window", self)
        close_window_action.setShortcut("Ctrl+Q")  
        close_window_action.setStatusTip("Close the current window")
        close_window_action.triggered.connect(self.close_current_window)
        file_menu.addAction(close_window_action)
        

        quit_action = QAction("Exit",self)
        file_menu.addAction(quit_action)
        quit_action.triggered.connect(self.quit_app)

 
        edit_menu = menu_bar.addMenu("Edit")

        undo_action = QAction("Undo",self)
        edit_menu.addAction(undo_action)
        undo_action.setShortcut("Ctrl+Z")
        undo_action.setStatusTip("Undo selected text ")
        undo_action.triggered.connect(self.text_edit.undo)

        redo_action = QAction("Redo", self)
        edit_menu.addAction(redo_action)
        redo_action.setShortcut("Ctrl+Y") 
        redo_action.setStatusTip("Redo")
        redo_action.triggered.connect(self.text_edit.redo)

        cut_action = QAction("Cut",self)
        edit_menu.addAction(cut_action)
        cut_action.setShortcut("Ctrl+X")
        cut_action.setStatusTip("Cut selected text to clipboard")
        cut_action.triggered.connect(self.cut_text)

        copy_action = QAction("Copy",self)
        edit_menu.addAction(copy_action)
        copy_action.setShortcut("Ctrl+C")
        copy_action.setStatusTip("Copy selected text to clipboard")
        copy_action.triggered.connect(self.copy_text)
        
        paste_action = QAction("Paste",self)
        edit_menu.addAction(paste_action)
        paste_action.setShortcut("Ctrl+V")
        paste_action.setStatusTip("Paste text from clipboard")
        paste_action.triggered.connect(self.paste_text)

        delete_action = QAction("delete",self)
        edit_menu.addAction(delete_action)
        delete_action.setShortcut("Delete")
        delete_action.setStatusTip("Delete selected text")
        delete_action.triggered.connect(self.delete_text)

        find_action = QAction("Find",self)
        edit_menu.addAction(find_action)
        find_action.setShortcut("ctrl+F")
        find_action.setStatusTip("Find text")
        find_action.triggered.connect(self.find_text)

        find_next_action = QAction("Find next",self)
        edit_menu.addAction(find_next_action)
        find_next_action.setShortcut("F3")
        find_next_action.setStatusTip("Find next occurrence of text")
        find_next_action.triggered.connect(self.find_next_text)

        find_previous_action = QAction("Find previous",self)
        edit_menu.addAction(find_previous_action)
        find_previous_action.setShortcut("Shift+F3")
        find_previous_action.setStatusTip("Find previous occurrence of text")
        find_previous_action.triggered.connect(self.find_previous_text)

        replace_action = QAction("Replace",self)
        edit_menu.addAction(replace_action)
        replace_action.setShortcut("Ctrl+H")
        replace_action.setStatusTip("Find and replace text")
        replace_action.triggered.connect(self.replace_text)

        go_to_action = QAction("Go to",self)
        edit_menu.addAction(go_to_action)
        go_to_action.setShortcut("Ctrl+G")
        go_to_action.setStatusTip("Go to line")
        go_to_action.triggered.connect(self.go_to_line)

        select_all_action = QAction("Select all",self)
        edit_menu.addAction(select_all_action)
        select_all_action.setShortcut("Ctrl+A")
        select_all_action.setStatusTip("Select all text")
        select_all_action.triggered.connect(self.select_all_text)

        time_date_action = QAction("Time/Date",self)
        edit_menu.addAction(time_date_action)
        time_date_action.setShortcut("F5")
        time_date_action.setStatusTip("Insert current time and date")
        time_date_action.triggered.connect(self.insert_current_time_date)

        import_image_action = QAction("Import Image", self)
        import_image_action.setShortcut("Ctrl+I")
        import_image_action.setStatusTip("Import an image into the current tab")
        import_image_action.triggered.connect(self.import_image)
        edit_menu.addAction(import_image_action)

        preview_action = QAction("Preview", self)
        preview_action.triggered.connect(self.preview_report)
        edit_menu.addAction(preview_action)

        template_action = QAction("Generate Template", self)
        template_action.triggered.connect(self.generate_template)
        edit_menu.addAction(template_action)
        
        font_action = QAction("Font",self)
        edit_menu.addAction(font_action)
        font_action.setShortcut("Ctrl+T")  
        font_action.setStatusTip("Change the font")
        font_action.triggered.connect(self.show_font_dialog)
        

        view_menu = menu_bar.addMenu("View")

        zoom_in_action = QAction("Zoom In", self)
        view_menu.addAction(zoom_in_action)
        zoom_in_action.setShortcut("Ctrl++")
        zoom_in_action.setStatusTip("Zoom in")
        zoom_in_action.triggered.connect(self.zoom_in)

        zoom_out_action = QAction("Zoom Out", self)
        view_menu.addAction(zoom_out_action)
        zoom_out_action.setShortcut("Ctrl+-")
        zoom_out_action.setStatusTip("Zoom out")
        zoom_out_action.triggered.connect(self.zoom_out)
        
        status_bar_action = QAction("Status Bar", self)
        view_menu.addAction(status_bar_action)
        status_bar_action.setStatusTip("Toggle status bar")
        status_bar_action.setCheckable(True)
        status_bar_action.setChecked(True)
        status_bar_action.triggered.connect(self.toggle_status_bar)

        word_wrap_action = QAction("Word Wrap", self)
        view_menu.addAction(word_wrap_action)
        word_wrap_action.setStatusTip("Toggle word wrap")
        word_wrap_action.setCheckable(True)
        word_wrap_action.setChecked(False)
        word_wrap_action.triggered.connect(self.toggle_word_wrap)
        


    def quit_app(self):
        sys.exit()

    def import_image(self):
        file_dialog = QFileDialog(self)
        file_path, _ = file_dialog.getOpenFileName(self, "Import Image", "", "Image Files (*.jpg *.png *.bmp)")
        if file_path:
            image_path = os.path.abspath(file_path)
            pixmap = QPixmap(image_path)

            width, ok = QInputDialog.getInt(self, "Image Width", "Enter new width:", pixmap.width())
        if ok:
            height = (pixmap.height() * width) // pixmap.width()
            pixmap = pixmap.scaled(width, height)

            image_format = QTextImageFormat()
            image_format.setWidth(pixmap.width())
            image_format.setHeight(pixmap.height())
            image_format.setName(image_path)

            cursor = self.text_edit.textCursor()
            cursor.insertImage(image_format)


    def convert_to_pdf(self):
        current_tab = self.text_edit.toPlainText()
        if not current_tab:
            return

        pdf_path, _ = QFileDialog.getSaveFileName(self, 'Save as PDF', '', 'PDF Files (*.pdf)')

        if pdf_path:
            printer = QPrinter(QPrinter.HighResolution)
            printer.setOutputFormat(QPrinter.PdfFormat)
            printer.setOutputFileName(pdf_path)

            document = QTextDocument()
            document.setPlainText(current_tab)

            cursor = QTextCursor(document)
            cursor.select(QTextCursor.Document)
            cursor.mergeCharFormat(QTextCharFormat())

            document.print_(printer)
            self.statusBar().showMessage(f'PDF saved as {pdf_path}', 3000)

    def open_report(self):
        file_dialog = QFileDialog(self)
        file_path, _ = file_dialog.getOpenFileName(self, "Open Report", "", "Text Files (*.txt);;All Files (*)")

        if file_path:
            with open(file_path, 'r') as file:
                report_content = file.read()
                new_report = QTextEdit()
                new_report.setPlainText(report_content)
                self.tab_widget.addTab(new_report, os.path.basename(file_path))
                self.tab_widget.setCurrentWidget(new_report)
                self.current_report = new_report

    

    def preview_report(self):
        if not self.current_report:
            return

        # Extract the QTextDocument from the QTextEdit
        preview_document = self.current_report.document()

        # Pass the QTextDocument to the PreviewDialog
        preview_dialog = PreviewDialog(preview_document)
        preview_dialog.exec_()


    def generate_template(self):
        # Define the report template
        template = """
        Report Title
        ============

        Date: {current_date}

        Author: {author_name}

        Introduction
        ------------
        This is the introduction section of your report.

        Section 1
        ---------
        Here you can add content for section 1.

        Section 2
        ---------
        And here goes the content for section 2.

        Conclusion
        ----------
        Finally, you can add a conclusion.

        """

        # Get user input for the report title and author name
        report_title, _ = QInputDialog.getText(self, "Report Title", "Enter the report title:")
        author_name, _ = QInputDialog.getText(self, "Author Name", "Enter your name:")

        # Replace placeholders with user input and set the template to the current tab
        template = template.format(current_date=QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss"), author_name=author_name)
        self.current_report.setPlainText(template)

        # Set the report title as the tab title
        if report_title:
            tab_index = self.tab_widget.currentIndex()
            self.tab_widget.setTabText(tab_index, report_title)

    def copy_text(self):
        selected_text = self.text_edit.textCursor().selectedText()
        clipboard = QApplication.clipboard()
        clipboard.setText(selected_text)

    def cut_text(self):
        cursor = self.text_edit.textCursor()
        selected_text = cursor.selectedText()
        clipboard = QApplication.clipboard()
        clipboard.setText(selected_text)
        cursor.removeSelectedText()

    def paste_text(self):
        clipboard = QApplication.clipboard()
        text_to_paste = clipboard.text()
        current_tab = self.tab_widget.currentWidget()
        current_tab.insertPlainText(text_to_paste)

    
    def delete_text(self):
        cursor = self.text_edit.textCursor()
        cursor.removeSelectedText()

    def find_text(self):
        find_dialog = QInputDialog.getText(self, "Find Text", "Find:")
        if find_dialog[1]:
            text_to_find = find_dialog[0]
            cursor = self.text_edit.textCursor()
            cursor.movePosition(QTextCursor.Start)
            cursor = self.text_edit.find(text_to_find, cursor)
            if not cursor.isNull():
                self.text_edit.setTextCursor(cursor)

    def find_next_text(self):
        cursor = self.text_edit.textCursor()
        cursor = self.text_edit.find(cursor.selectedText(), cursor)
        if not cursor.isNull():
            self.text_edit.setTextCursor(cursor)

    def find_previous_text(self):
        cursor = self.text_edit.textCursor()
        cursor.movePosition(QTextCursor.Start, QTextCursor.KeepAnchor)
        cursor = self.text_edit.find(cursor.selectedText(), cursor)
        if not cursor.isNull():
            self.text_edit.setTextCursor(cursor)

    def replace_text(self):
        replace_dialog = QInputDialog.getText(self, "Replace Text", "Find and Replace (e.g., find|replace):")
        if replace_dialog[1]:
            find_text, replace_text = replace_dialog[0].split('|')
            cursor = self.text_edit.textCursor()
            cursor.beginEditBlock()
            cursor.movePosition(QTextCursor.Start)
            while cursor.movePosition(QTextCursor.NextWord, QTextCursor.KeepAnchor):
                if cursor.selectedText() == find_text:
                    cursor.removeSelectedText()
                    cursor.insertText(replace_text)
            cursor.endEditBlock()

    def go_to_line(self):
        line_dialog = QInputDialog.getInt(self, "Go To Line", "Line Number:", 1, 1, 999999, 1)
        if line_dialog[1]:
            line_number = line_dialog[0]
            cursor = self.text_edit.textCursor()
            cursor.movePosition(QTextCursor.Start)
            cursor.movePosition(QTextCursor.NextBlock, QTextCursor.MoveAnchor, line_number - 1)
            self.text_edit.setTextCursor(cursor)

    def select_all_text(self):
        self.text_edit.selectAll()

    def insert_current_time_date(self):
        current_datetime = QDateTime.currentDateTime()
        formatted_datetime = current_datetime.toString("yyyy-MM-dd hh:mm:ss")
        cursor = self.text_edit.textCursor()
        cursor.insertText(formatted_datetime)

    def toggle_status_bar(self):
        if self.statusBar().isVisible():
            self.statusBar().setVisible(False)
        else:
            self.statusBar().setVisible(True)

    def toggle_word_wrap(self):
        self.text_edit.setLineWrapMode(QTextEdit.WidgetWidth if not self.text_edit.lineWrapMode() else QTextEdit.NoWrap)

    def zoom_in(self):
        self.text_edit.zoomIn(2)

    def zoom_out(self):
        self.text_edit.zoomOut(2)


    # Create a new tab with a QTextEdit widget    
    def addNewTab(self):
        self.text_edit = QTextEdit()
        tab_index = self.tab_widget.addTab(self.text_edit, "Untitled")
        self.tab_widget.setCurrentIndex(tab_index)
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.closeTab)


    def addNewWindow(self):
        new_window = Mainwindow()
        new_window.show()
        self.windows.append(new_window)

    def save_text(self):
        current_tab = self.tab_widget.currentWidget()
        text = current_tab.toPlainText()
        tab_index = self.tab_widget.currentIndex()
        tab_text = self.tab_widget.tabText(tab_index)

        if tab_text == "Untitled":
            self.save_text_as()
        else:
            with open(tab_text, 'w') as file:
                file.write(text)

    def save_text_as(self):
        current_tab = self.tab_widget.currentWidget()
        text = current_tab.toPlainText()

        
        file_dialog = QFileDialog(self)
        file_path, _ = file_dialog.getSaveFileName(self, "Save File As", "", "Text Files (*.txt);;All Files (*)")

        if file_path:
            with open(file_path, 'w') as file:
                file.write(text)


    def closeTab(self, index):
        self.tab_widget.removeTab(index)

    def show_font_dialog(self):
        font, ok = QFontDialog.getFont()
        print(font, ok) 
        if ok:
            self.text_edit.setFont(True)
   

    def save_all_tabs(self):
        for index in range(self.tab_widget.count()):
            self.tab_widget.setCurrentIndex(index)
            self.save_text()

    def page_setup(self):
        printer = QPrinter(QPrinter.HighResolution)
        page_setup_dialog = QPageSetupDialog(printer, self)
        if page_setup_dialog.exec_() == QPageSetupDialog.Accepted:
            pass  

    def print_tab(self):
        printer = QPrinter(QPrinter.HighResolution)
        print_dialog = QPrintDialog(printer, self)
        if print_dialog.exec_() == QPrintDialog.Accepted:
            self.text_edit.print(printer)

    def close_current_tab(self):
        current_index = self.tab_widget.currentIndex()
        if current_index != -1:
            self.tab_widget.removeTab(current_index)

    def close_current_window(self):
        self.close()