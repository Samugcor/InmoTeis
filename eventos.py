'''
Eventos que no tienen que ver con la gestion dde la db
'''
import sys
import time
import re

import conexion
from PyQt6 import QtWidgets
from PyQt6.QtGui import QIcon

import var


class Eventos:
    #Pop up salir
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

    #Cargar valores
    def cargarProvincias(self):
        var.ui.cmbProvCli.clear()
        listado=conexion.Conexion.listaProv(self)
        var.ui.cmbProvCli.addItems(listado)

    def cargarMunicipios(self):
        provincia=var.ui.cmbProvCli.currentText()
        var.ui.cmbMunicipioCli.clear()
        listado=conexion.Conexion.listaMuni(provincia)
        var.ui.cmbMunicipioCli.addItems(listado)

    #Validacion
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

    def abrirCalendar(op):
        try:
            var.panel = op
            var.uiCalendar.show()
        except Exception as error:
            print("error en abrir calendar ", error)

    def cargaFecha(qDate):
        try:
            data = ('{:02d}/{:02d}/{:4d}'.format(qDate.day(), qDate.month(), qDate.year()))
            if var.panel == var.ui.panPrincipal.currentIndex():
                var.ui.txtAltaCliente.setText(str(data))
            time.sleep(0.5)
            var.uiCalendar.hide()
            return data
        except Exception as error:
            print("error en cargar fecha: ", error)

    def validarMail(mail):
        mail = mail.lower()
        regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'
        if re.match(regex, mail):
            return True
        else:
            return False