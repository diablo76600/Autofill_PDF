# -*- coding: utf-8 -*-


import sys
from pathlib import Path
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QIntValidator
from PyQt5.QtCore import Qt
from pypdf import PdfReader, PdfWriter

# Set localization in French
locale = QtCore.QLocale(QtCore.QLocale.Language.French, QtCore.QLocale.Country.France)




class MainWindow(QtWidgets.QMainWindow):
    def __init__(self) -> None:
        """Initialize the main application window with various UI elements and settings."""
        super().__init__()
        self.setLocale(locale)
        self.today = QtCore.QDate.currentDate() # Get the current date
        onlyInt = QIntValidator() # Create a validator for integers
        onlyInt.setRange(0, 9999999) # Set the range for the integer validator
        self.resize(600, 250) # Resize the main window
        self.gridLayoutWidget = QtWidgets.QWidget(self) # Create a widget for the grid layout
        self.gridLayoutWidget.setGeometry(QtCore.QRect(30, 20, 580, 230)) # Set the geometry of the widget
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget) # Create a grid layout within the widget
        # Widgets Date
        self.label_date = QtWidgets.QLabel(self.gridLayoutWidget)
        self.gridLayout.addWidget(self.label_date, 0, 0, 1, 1)
        self.dateEdit = QtWidgets.QDateEdit(self.gridLayoutWidget)
        self.dateEdit.setDisplayFormat("dddd dd MMMM yyyy") 
        self.dateEdit.setFixedWidth(200)
        self.dateEdit.setCalendarPopup(True)
        self.dateEdit.setDate(self.today)
        self.gridLayout.addWidget(self.dateEdit, 0, 1, 1, 1)
        # Widgets Pdf file
        self.label_pdf_file = QtWidgets.QLabel(self.gridLayoutWidget)
        self.gridLayout.addWidget(self.label_pdf_file, 1, 0, 1, 1)
        self.lineEdit_pdf_file = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.lineEdit_pdf_file.setClearButtonEnabled(True)
        self.gridLayout.addWidget(self.lineEdit_pdf_file, 1, 1, 1, 1)
        # Widgets Number
        self.label_number = QtWidgets.QLabel(self.gridLayoutWidget)
        self.gridLayout.addWidget(self.label_number, 2, 0, 1, 1)
        self.lineEdit_number = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.lineEdit_number.setFixedWidth(100)
        self.lineEdit_number.setValidator(onlyInt)
        self.lineEdit_number.setClearButtonEnabled(True)
        self.gridLayout.addWidget(self.lineEdit_number, 2, 1, 1, 1)
        # Widget Button save pdf
        self.pushButton_select_pdf = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_select_pdf.clicked.connect(self.select_pdf_file)
        self.pushButton_select_pdf.setFocus()
        self.gridLayout.addWidget(self.pushButton_select_pdf, 1, 2, 1, 1)
        self.pushButton_save_pdf = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_save_pdf.setMaximumSize(QtCore.QSize(120, 24))
        self.pushButton_save_pdf.clicked.connect(self.save_pdf_file)
        #
        self.gridLayout.addWidget(
            self.pushButton_save_pdf, 3, 1, 1, 1, alignment=Qt.AlignmentFlag.AlignHCenter
        )
        self.setCentralWidget(self.gridLayoutWidget) # Set the central widget
        self.retranslateUi() # Set the text for UI elements

    def retranslateUi(self) -> None:
        """Set the text for various UI elements in the application."""
        self.setWindowTitle("Suivi de colis")
        self.label_date.setText("Date d'envoi :")
        self.pushButton_select_pdf.setText("Choisir PDF")
        self.label_pdf_file.setText("Fichier PDF :")
        self.label_number.setText("Numéro :")
        self.pushButton_save_pdf.setText("Enregistrer PDF")


class ModifyPdf(MainWindow):
    def __init__(self) -> None:
        """Initialize the object."""
        super().__init__()

    def select_pdf_file(self) -> None:
        """Open a file dialog to select a PDF file and set the selected file path in the QLineEdit."""
        current_file, _ = QtWidgets.QFileDialog.getOpenFileName(
            parent=self,
            caption="Selectionnez le fichier PDF",
            directory=str(Path.home()),
            filter="Pdf (*.pdf *.PDF);;All files (*.*)",
            options=QtWidgets.QFileDialog.DontUseNativeDialog
        )
        self.lineEdit_pdf_file.setText(current_file)

    def select_destination_file(self) -> str:
        """Open a file dialog to select a destination path for saving a PDF file."""
        new_file, _ = QtWidgets.QFileDialog.getSaveFileName(
            parent=self,
            caption="Enregistrer le fichier PDF",
            directory=f"{str(Path.home())}/Nouveau_fichier.pdf",
        )
        return new_file

    def validate_fields(self) -> bool:
            """Check if the PDF file path and number fields are not empty. """
            return bool(self.lineEdit_pdf_file.text() and self.lineEdit_number.text())

    def generate_data_dict(self) -> dict[str, str]:
        """Generate a dictionary containing data from the UI elements."""
        return {
            "dactuelle": self.today.toString("MMMM yyyy"),
            "ddepot": self.dateEdit.text(),
            "num": self.lineEdit_number.text(),
        }

    def save_pdf_file(self) -> None:
        """Save a modified PDF file with user-provided data if fields are valid, show warnings otherwise."""
        if not self.validate_fields():
            QtWidgets.QMessageBox.warning(
                self, "Problème !!", "Veuillez saisir tous les champs !!"
            )
            return
        data_dict = self.generate_data_dict()
        if new_file := self.select_destination_file():
            self.save_modified_pdf_file(self.lineEdit_pdf_file.text(), new_file, data_dict)
            QtWidgets.QMessageBox.information(
                self, "Sauvegarde", f"Fichier {new_file} enregistré."
            )

    def save_modified_pdf_file(self, pdf_file, new_file, data_dict) -> None:
        """Save a modified PDF file with updated form field values."""
        reader = PdfReader(pdf_file)
        writer = PdfWriter()
        writer.append(reader)
        writer.update_page_form_field_values(
            writer.pages[0], data_dict, flags=1
        )
        writer.write(new_file)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    # Translate
    translator = QtCore.QTranslator()
    traduction = QtCore.QLibraryInfo.location(QtCore.QLibraryInfo.TranslationsPath)
    translator.load("qtbase_fr.qm", traduction)
    app.installTranslator(translator)
    modify_pdf = ModifyPdf()
    modify_pdf.show()
    sys.exit(app.exec())
