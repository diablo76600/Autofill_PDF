# -*- coding: utf-8 -*-


import sys
from pathlib import Path
from PyQt6 import QtCore, QtGui, QtWidgets, QtPdf
from PyQt6.QtPdf import QPdfDocument
from PyQt6.QtPdfWidgets import QPdfView
from PyQt6.QtGui import QIntValidator
from PyQt6.QtCore import Qt
from fillpdf import fillpdfs
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
        self.pushButton_choice.clicked.connect(self.select_pdf)
        self.gridLayout.addWidget(self.pushButton_choice, 1, 2, 1, 1)
        self.label_pdf_file = QtWidgets.QLabel(self.gridLayoutWidget)
        self.gridLayout.addWidget(self.label_pdf_file, 1, 0, 1, 1)
        self.label_number = QtWidgets.QLabel(self.gridLayoutWidget)
        self.gridLayout.addWidget(self.label_number, 2, 0, 1, 1)
        self.pushButton_save = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_save.setMaximumSize(QtCore.QSize(120, 24))
        self.pushButton_save.clicked.connect(self.save_pdf)
        self.gridLayout.addWidget(self.pushButton_save, 3, 1, 1, 1, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.setCentralWidget(self.gridLayoutWidget)
        self.retranslateUi()

    def retranslateUi(self):
        self.setWindowTitle("Remplissage Automatique de fichiers PDF")
        self.label_date.setText("Date d'envoi :")
        self.pushButton_choice.setText("Choisir PDF")
        self.label_pdf_file.setText("Fichier PDF :")
        self.label_number.setText("Numéro :")
        self.pushButton_save.setText("Enregistrer PDF")

class ModifyPdf(MainWindow):
    def __init__(self):
        super().__init__()

    def select_pdf(self):
        current_file, _ = QtWidgets.QFileDialog.getOpenFileName(
            parent=self, caption="Selectionnez le fichier PDF", directory=str(Path.home()), filter="*.pdf")
        self.lineEdit_pdf.setText(current_file)

    def select_destination(self):
        new_file, _ = QtWidgets.QFileDialog.getSaveFileName(
            parent=self,
            caption="Sauvegarder le fichier PDF",
            directory=f"{str(Path.home())}/Nouveau_fichier.pdf",
        )
        return new_file
    
    def control_fields(self):
        return bool(self.lineEdit_pdf.text() and self.lineEdit_number.text())

    def save_pdf(self):
        if self.control_fields():
            formatted_date = self.today.toPyDate().strftime("%b %Y")
            sending_date = self.dateEdit.text()
            pdf_file = self.lineEdit_pdf.text()
            number = self.lineEdit_number.text()
            data_dict = {"dactuelle": formatted_date, "ddepot": sending_date, "num": number}
        else:
            QtWidgets.QMessageBox.warning(self, "Problème !!", "Veuillez remplir tous les champs !!")
            return
        if new_file := self.select_destination():
            fillpdfs.write_fillable_pdf(pdf_file, new_file, data_dict, flatten=False)
            QtWidgets.QMessageBox.information(self, "Sauvegarde", f"Fichier {new_file} enregistré.")


if __name__ == "__main__":
    myApp = QtWidgets.QApplication(sys.argv)
    modify_pdf = ModifyPdf()
    modify_pdf.show()
    sys.exit(myApp.exec())
