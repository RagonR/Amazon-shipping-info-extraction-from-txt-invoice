import os
import sys
import xlrd
from xlsxwriter import Workbook

from PyQt5 import QtCore, QtGui, QtWidgets
import FileBrowser
import MailCSVMaker


class Ui_Dialog(object):
    def __init__(self):
        self.error_dialog = QtWidgets.QErrorMessage()
        self.verticalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.pushButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.textBrowser = QtWidgets.QTextBrowser(self.verticalLayoutWidget)
        self.pushButton_2 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.fb = FileBrowser.MyFileBrowser()

    def setup_ui(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setWindowModality(QtCore.Qt.WindowModal)
        Dialog.resize(225, 235)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("ExcelEditor.ico"), QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        Dialog.setStyleSheet("background-color: rgb(30, 82, 34);")
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(30, 0, 161, 229))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout.setObjectName("verticalLayout")
        self.pushButton.setMouseTracking(False)
        self.pushButton.setStyleSheet("QPushButton {\n"
                                      "    font: 87 10pt \"Arial Black\";\n"
                                      "    color: #333;\n"
                                      "    border: 15px solid #308234;\n"
                                      "    border-radius: 20px;\n"
                                      "    border-style: outset;\n"
                                      "    background: qradialgradient(\n"
                                      "        cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4,\n"
                                      "        radius: 1.35, stop: 0 #308234, stop: 1 #48c34e\n"
                                      "        );\n"
                                      "    padding: 5px;\n"
                                      "    }\n"
                                      "\n"
                                      "QPushButton:hover {\n"
                                      "    background: qradialgradient(\n"
                                      "        cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4,\n"
                                      "        radius: 1.35, stop: 0 #48c34e, stop: 1 #308234\n"
                                      "        );\n"
                                      "    }\n"
                                      "\n"
                                      "QPushButton:pressed {\n"
                                      "    border-style: inset;\n"
                                      "    background: qradialgradient(\n"
                                      "        cx: 0.4, cy: -0.1, fx: 0.4, fy: -0.1,\n"
                                      "        radius: 1.35, stop: 0 #4cf4ff, stop: 1 #ddd\n"
                                      "        );\n"
                                      "    }")
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)
        self.textBrowser.setStyleSheet("font: 87 10pt \"Arial Black\";")
        self.textBrowser.setEnabled(True)
        self.textBrowser.setObjectName("plainTextEdit")
        self.verticalLayout.addWidget(self.textBrowser)
        self.pushButton_2.setStyleSheet("QPushButton {\n"
                                        "    font: 87 10pt \"Arial Black\";\n"
                                        "    color: #333;\n"
                                        "    border: 15px solid #308234;\n"
                                        "    border-radius: 20px;\n"
                                        "    border-style: outset;\n"
                                        "    background: qradialgradient(\n"
                                        "        cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4,\n"
                                        "        radius: 1.35, stop: 0 #308234, stop: 1 #48c34e\n"
                                        "        );\n"
                                        "    padding: 5px;\n"
                                        "    }\n"
                                        "\n"
                                        "QPushButton:hover {\n"
                                        "    background: qradialgradient(\n"
                                        "        cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4,\n"
                                        "        radius: 1.35, stop: 0 #48c34e, stop: 1 #308234\n"
                                        "        );\n"
                                        "    }\n"
                                        "\n"
                                        "QPushButton:pressed {\n"
                                        "    border-style: inset;\n"
                                        "    background: qradialgradient(\n"
                                        "        cx: 0.4, cy: -0.1, fx: 0.4, fy: -0.1,\n"
                                        "        radius: 1.35, stop: 0 #4cf4ff, stop: 1 #ddd\n"
                                        "        );\n"
                                        "    }")
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout.addWidget(self.pushButton_2)

        self.retranslate_ui(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        self.pushButton.clicked.connect(self.get_file_browser)
        self.pushButton_2.clicked.connect(self.edit_selected_excel)

    def get_file_browser(self):
        try:
            self.fb.closeEvent = self.close_event
            self.fb.show()
        except:
            print("failed")

    def close_event(self, event):
        self.set_text_browser()

    def set_text_browser(self):
        self.textBrowser.clear()
        self.textBrowser.insertPlainText(os.path.basename(FileBrowser.Data.file_path))

    def edit_selected_excel(self):
        if FileBrowser.Data.file_path.endswith('.xlsx') | FileBrowser.Data.file_path.endswith('.XLSX'):
            try:
                MailCSVMaker.get_data_from_file(FileBrowser.Data.file_path)
            except Exception as e:  # work on python 3.x
                print('Failed: ' + str(e))
        else:
            self.error_dialog.showMessage('Selected file is not txt')

    def retranslate_ui(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Excel Editor"))
        self.pushButton.setText(_translate("Dialog", "Select File"))
        self.pushButton_2.setText(_translate("Dialog", "Execute"))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog(None, QtCore.Qt.WindowSystemMenuHint |
                               QtCore.Qt.WindowTitleHint |
                               QtCore.Qt.WindowMinimizeButtonHint |
                               QtCore.Qt.WindowCloseButtonHint |
                               QtCore.Qt.WindowStaysOnTopHint)
    ui = Ui_Dialog()
    ui.setup_ui(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
