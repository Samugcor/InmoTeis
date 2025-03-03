# Form implementation generated from reading ui file '.\\templates\\dlgAbout.ui'
#
# Created by: PyQt6 UI code generator 6.7.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        Dialog.resize(400, 199)
        Dialog.setMaximumSize(QtCore.QSize(400, 200))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(".\\\\templates\\../img/house.svg"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        Dialog.setWindowIcon(icon)
        Dialog.setModal(True)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.btnCerrarAbout = QtWidgets.QPushButton(parent=Dialog)
        self.btnCerrarAbout.setObjectName("btnCerrarAbout")
        self.gridLayout.addWidget(self.btnCerrarAbout, 4, 4, 1, 1)
        self.label_2 = QtWidgets.QLabel(parent=Dialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 3, 1, 1)
        self.label_3 = QtWidgets.QLabel(parent=Dialog)
        self.label_3.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignTop)
        self.label_3.setWordWrap(True)
        self.label_3.setOpenExternalLinks(True)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 3, 1, 2)
        self.label_4 = QtWidgets.QLabel(parent=Dialog)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 3, 3, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 2, 1, 1)
        self.label = QtWidgets.QLabel(parent=Dialog)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setTextFormat(QtCore.Qt.TextFormat.RichText)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 3, 1, 2)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout.addItem(spacerItem1, 2, 5, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout.addItem(spacerItem2, 2, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(parent=Dialog)
        self.label_5.setMaximumSize(QtCore.QSize(150, 150))
        self.label_5.setText("")
        self.label_5.setPixmap(QtGui.QPixmap(".\\\\templates\\../img/realestatehouse_101105.png"))
        self.label_5.setScaledContents(True)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 0, 1, 4, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.btnCerrarAbout.setText(_translate("Dialog", "Cerrar"))
        self.label_2.setText(_translate("Dialog", "Version 1.0"))
        self.label_3.setText(_translate("Dialog", "InmoTeis es una aplicación de gestión inmobiliaria."))
        self.label_4.setText(_translate("Dialog", "Copyright (c)  2024"))
        self.label.setText(_translate("Dialog", "Inmobiliaria Teis"))
