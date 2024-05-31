# -*- coding: utf-8 -*-


import sys
from pathlib import Path
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QIntValidator
from PyQt5.QtCore import Qt
from PyPDF2 import PdfReader, PdfWriter
import locale

# Définir la localisation en français
locale.setlocale(locale.LC_TIME, "fr_FR.UTF-8")


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.today = QtCore.QDate.currentDate()
        onlyInt = QIntValidator()
        onlyInt.setRange(0, 9999999)
        self.resize(600, 250)
        self.gridLayoutWidget = QtWidgets.QWidget(self)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(30, 20, 541, 201))
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.label_date = QtWidgets.QLabel(self.gridLayoutWidget)
        self.gridLayout.addWidget(self.label_date, 0, 0, 1, 1)
        self.lineEdit_pdf = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.gridLayout.addWidget(self.lineEdit_pdf, 1, 1, 1, 1)
        self.dateEdit = QtWidgets.QDateEdit(self.gridLayoutWidget)
        self.dateEdit.setCalendarPopup(True)
        self.dateEdit.setDate(self.today)
        self.gridLayout.addWidget(self.dateEdit, 0, 1, 1, 1)
        self.label_destination = QtWidgets.QLabel(self.gridLayoutWidget)
        self.gridLayout.addWidget(self.label_destination, 3, 0, 1, 1)
        self.lineEdit_number = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.lineEdit_number.setValidator(onlyInt)
        self.lineEdit_number.setClearButtonEnabled(True)
        self.gridLayout.addWidget(self.lineEdit_number, 2, 1, 1, 1)
        self.pushButton_choice = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_choice.clicked.connect(self.select_pdf_file)
        self.gridLayout.addWidget(self.pushButton_choice, 1, 2, 1, 1)
        self.label_pdf_file = QtWidgets.QLabel(self.gridLayoutWidget)
        self.gridLayout.addWidget(self.label_pdf_file, 1, 0, 1, 1)
        self.label_number = QtWidgets.QLabel(self.gridLayoutWidget)
        self.gridLayout.addWidget(self.label_number, 2, 0, 1, 1)
        self.pushButton_save = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_save.setMaximumSize(QtCore.QSize(120, 24))
        self.pushButton_save.clicked.connect(self.save_pdf_file)
        self.gridLayout.addWidget(
            self.pushButton_save, 3, 1, 1, 1, alignment=Qt.AlignmentFlag.AlignHCenter
        )
        self.setCentralWidget(self.gridLayoutWidget)
        self.retranslateUi()

    def retranslateUi(self):
        self.setWindowTitle("Suivi de colis")
        self.label_date.setText("Date d'envoi :")
        self.pushButton_choice.setText("Choisir PDF")
        self.label_pdf_file.setText("Fichier PDF :")
        self.label_number.setText("Numéro :")
        self.pushButton_save.setText("Enregistrer PDF")


class ModifyPdf(MainWindow):
    def __init__(self):
        super().__init__()

    def select_pdf_file(self):
        current_file, _ = QtWidgets.QFileDialog.getOpenFileName(
            parent=self,
            caption="Selectionnez le fichier PDF",
            directory=str(Path.home()),
            filter="Pdf (*.pdf *.PDF);;All files (*.*)"
        )
        self.lineEdit_pdf.setText(current_file)

    def select_destination_file(self):
        new_file, _ = QtWidgets.QFileDialog.getSaveFileName(
            parent=self,
            caption="Enregistrer le fichier PDF",
            directory=f"{str(Path.home())}/Nouveau_fichier.pdf",
        )
        return new_file

    def validate_fields(self):
        return bool(self.lineEdit_pdf.text() and self.lineEdit_number.text())

    def generate_data_dict(self):
        return {
            "dactuelle": self.today.toPyDate().strftime("%b %Y"),
            "ddepot": self.dateEdit.text(),
            "num": self.lineEdit_number.text(),
        }

    def save_pdf_file(self):
        if not self.validate_fields():
            QtWidgets.QMessageBox.warning(
                self, "Problème !!", "Veuillez remplir tous les champs !!"
            )
            return
        data_dict = self.generate_data_dict()
        if new_file := self.select_destination_file():
            self.save_modified_pdf_file(self.lineEdit_pdf.text(), new_file, data_dict)
            QtWidgets.QMessageBox.information(
                self, "Sauvegarde", f"Fichier {new_file} enregistré."
            )

    def save_modified_pdf_file(self, pdf_file, new_file, data_dict):
        ReadOnly = False
        reader = PdfReader(pdf_file)
        writer = PdfWriter()
        page = reader.pages[0]
        writer.add_page(page)
        writer.update_page_form_field_values(
            writer.pages[0], data_dict, flags=ReadOnly # type: ignore
        )
        with open(new_file, "wb") as output_stream:
            writer.write(output_stream)


if __name__ == "__main__":
    myApp = QtWidgets.QApplication(sys.argv)
    modify_pdf = ModifyPdf()
    modify_pdf.show()
    sys.exit(myApp.exec())
