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

    def validarDNIcli(dni):
        try:
            dni = str(dni).upper()
            var.ui.txtDniCliente.setText(str(dni))
            tabla = "TRWAGMYFPDXBNJZSQVHLCKE"
            dig_ext = "XYZ"
            reemp_dig_ext = {'X': '0', 'Y': '1', 'Z': '2'}
            numeros = "1234567890"
            if len(dni) == 9:
                dig_control = dni[8]
                dni = dni[:8]
                if dni[0] in dig_ext:
                    dni = dni.replace(dni[0], reemp_dig_ext[dni[0]])

                if len(dni) == len([n for n in dni if n in numeros]) and tabla[int(dni) % 23] == dig_control:
                    var.ui.txtDniCliente.setStyleSheet("background-color:rgb(255, 255, 222);")
                    return True
                else:
                    return False
            else:
                return False

        except Exception as error:
            print("error en validar dni ", error)