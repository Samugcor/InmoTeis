'''
Eventos que no tienen que ver con la gestion dde la db
'''
import sys
import conexion
from PyQt6 import QtWidgets
from PyQt6.QtGui import QIcon

import var


class Eventos:
    def mensajeSalir(self):
        mbox =QtWidgets.QMessageBox()
        mbox.setWindowIcon(QIcon('./img/house.svg'))
        mbox.setIcon(QtWidgets.QMessageBox.Icon.Question)
        mbox.setWindowTitle('Salir')
        mbox.setText('¿Desea usted salir?')
        mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
        mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.No)
        mbox.button(QtWidgets.QMessageBox.StandardButton.Yes).setText('Si')
        mbox.button(QtWidgets.QMessageBox.StandardButton.No).setText('No')

        if mbox.exec() == QtWidgets.QMessageBox.StandardButton.Yes:
            sys.exit()
        else:
            mbox.hide()

    def cargarProvincias(self):
        var.ui.cmbProvincia.clear()
        listado=conexion.Conexion.listaProv(self)
        var.ui.cmbProvincia.addItems(listado)

    def cargarMunicipios(self):
        var.ui.cmbMunicipio.clear()
        listado=conexion.Conexion.listaMuni(self)
        var.ui.cmbMunicipio.addItems(listado)