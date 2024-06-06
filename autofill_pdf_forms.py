# -*- coding: utf-8 -*-


import sys
from pathlib import Path
from PyQt5 import QtCore, QtWidgets, QtGui
from pypdf import PdfReader, PdfWriter
import locale
# Set localization in French
locale.setlocale(locale.LC_TIME, "fr_FR.UTF-8")


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.today = QtCore.QDate.currentDate()
        self.init_ui()
        self.retranslate_ui()

    def init_ui(self) -> None:
        """Initialize the UI elements."""
        self.resize(600, 250)
        central_widget = QtWidgets.QWidget(self)
        layout = QtWidgets.QGridLayout(central_widget)

        # Widgets Date
        self.date_label = QtWidgets.QLabel(self)
        layout.addWidget(self.date_label, 0, 0, 1, 1)
        self.date_edit = QtWidgets.QDateEdit(calendarPopup=True)
        self.date_edit.setDisplayFormat("dddd dd MMMM yyyy")
        self.date_edit.setFixedWidth(200)
        self.date_edit.setDate(self.today)
        layout.addWidget(self.date_edit, 0, 1, 1, 1)

        # Widgets PDF file
        self.pdf_file_label = QtWidgets.QLabel(self)
        layout.addWidget(self.pdf_file_label, 1, 0, 1, 1)
        self.pdf_file_line_edit = QtWidgets.QLineEdit(self)
        self.pdf_file_line_edit.setClearButtonEnabled(True)
        layout.addWidget(self.pdf_file_line_edit, 1, 1, 1, 1)

        # Widgets Number
        self.number_label = QtWidgets.QLabel(self)
        layout.addWidget(self.number_label, 2, 0, 1, 1)
        self.number_line_edit = QtWidgets.QLineEdit(self)
        self.number_line_edit.setFixedWidth(100)
        self.number_line_edit.setValidator(QtGui.QIntValidator(0, 9999999))
        self.number_line_edit.setClearButtonEnabled(True)
        layout.addWidget(self.number_line_edit, 2, 1, 1, 1)

        # Widget Button select PDF
        self.select_pdf_button = QtWidgets.QPushButton(self)
        self.select_pdf_button.clicked.connect(self.select_pdf_file)
        layout.addWidget(self.select_pdf_button, 1, 2, 1, 1)

        # Widget Button save PDF
        self.save_pdf_button = QtWidgets.QPushButton(self)
        self.save_pdf_button.setMaximumSize(QtCore.QSize(120, 24))
        self.save_pdf_button.clicked.connect(self.save_new_pdf)
        layout.addWidget(self.save_pdf_button, 3, 1, 1, 1, QtCore.Qt.AlignmentFlag.AlignHCenter)

        self.select_pdf_button.setFocus()
        self.setCentralWidget(central_widget)

    def retranslate_ui(self) -> None:
        """Set the text for UI elements."""
        self.setWindowTitle("Suivi de colis")
        self.date_label.setText("Date d'envoi:")
        self.date_edit.setToolTip("Sélectionnez la date d'envoi")
        self.pdf_file_label.setText("Fichier PDF:")
        self.number_label.setText("Numéro:")
        self.select_pdf_button.setText("Choisir PDF")
        self.save_pdf_button.setText("Enregistrer PDF")

    def select_pdf_file(self) -> None:
        """Open a file dialog to select a PDF file."""
        pdf_file, _ = QtWidgets.QFileDialog.getOpenFileName(
            self,
            "Sélectionnez le fichier PDF",
            str(Path.home()),
            "Pdf (*.pdf *.PDF);;Tous (*.*)",
            options=QtWidgets.QFileDialog.DontUseNativeDialog,
        )
        if pdf_file:
            self.pdf_file_line_edit.setText(pdf_file)

    def select_destination_file(self) -> str:
        """Open a file dialog to select a destination path for saving a PDF file."""
        destination_file, _ = QtWidgets.QFileDialog.getSaveFileName(
            self,
            "Enregistrer le fichier PDF",
            f"{str(Path.home())}/Nouveau_fichier.pdf",
            options=QtWidgets.QFileDialog.DontUseNativeDialog
        )
        return destination_file

    def validate_fields(self) -> bool:
        """Check if the PDF file path and number fields are not empty."""
        return bool(self.pdf_file_line_edit.text() and self.number_line_edit.text())

    def generate_data_dict(self) -> dict[str, str]:
        """Generate a dictionary containing data from the UI elements."""
        return {
            "dactuelle": self.today.toString("MMMM yyyy"),
            "ddepot": self.date_edit.text(),
            "num": self.number_line_edit.text(),
        }

    def create_new_pdf(self, pdf_file: str, data_dict: dict[str, str]) -> PdfWriter:
        """Create a new PDF file with updated form field values."""
        with open(pdf_file, "rb") as file:
            pdf_reader = PdfReader(file)
            pdf_writer = PdfWriter()
            pdf_writer.append(pdf_reader)
            pdf_writer.update_page_form_field_values(pdf_writer.pages[0], data_dict)
            return pdf_writer

    @QtCore.pyqtSlot()
    def save_new_pdf(self) -> None:
        """Save a modified PDF file with updated form field values."""
        if not self.validate_fields():
            QtWidgets.QMessageBox.warning(self, "Problème !!", "Veuillez saisir tous les champs !!")
            return

        data_dict = self.generate_data_dict()
        pdf_file = self.pdf_file_line_edit.text()

        if destination_file := self.select_destination_file():
            with open(destination_file, "wb") as file:
                pdf_writer = self.create_new_pdf(pdf_file, data_dict)
                pdf_writer.write(file)
            QtWidgets.QMessageBox.information(self, "Sauvegarde", f"Fichier {destination_file} enregistré.")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    # Translate
    translator = QtCore.QTranslator()
    translation_path = QtCore.QLibraryInfo.location(QtCore.QLibraryInfo.TranslationsPath)
    translator.load("qtbase_fr.qm", translation_path)
    app.installTranslator(translator)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
