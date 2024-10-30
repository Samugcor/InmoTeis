from PyQt6 import QtWidgets, QtCore
from PyQt6.QtGui import QIcon

import conexion
import eventos
import var
import venAux

class Propiedades():
    def altaTipoPropiedades(self):
        try:
            tipo = var.dlggestion.ui.txtGestTipoProp.text()
            tipo = tipo.capitalize()
            print(tipo)

            if conexion.Conexion.altaTipoPropiedad(tipo):
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowIcon(QIcon('./img/house.svg'))
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setWindowTitle('Aviso')
                mbox.setText('Tipo de propiedad "'+tipo+'" añadido')
                mbox.setStandardButtons(
                    QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')

                mbox.exec()
                eventos.Eventos.cargarTipoPropiedad(self)
                var.dlggestion.ui.txtGestTipoProp.setText('')

            else:
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowIcon(QIcon('./img/house.svg'))
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
                mbox.setWindowTitle('Aviso')
                mbox.setText('Error al añadir tipo de propiedad. Compruebe que el tipo no exista')
                mbox.setStandardButtons(
                    QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')

                mbox.exec()
        except Exception as e:
            print("Error en altaTipoPropiedades (propiedades.py)",e)

    def bajaTipoPropiedades(self):
        try:
            tipo = var.dlggestion.ui.txtGestTipoProp.text()
            tipo = tipo.capitalize()
            print(tipo)

            if conexion.Conexion.bajaTipoPropiedad(tipo):
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowIcon(QIcon('./img/house.svg'))
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setWindowTitle('Aviso')
                mbox.setText('Tipo de propiedad "'+tipo+'" eliminado')
                mbox.setStandardButtons(
                    QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')

                mbox.exec()
                eventos.Eventos.cargarTipoPropiedad(self)
                var.dlggestion.ui.txtGestTipoProp.setText('')

            else:
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowIcon(QIcon('./img/house.svg'))
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
                mbox.setWindowTitle('Aviso')
                mbox.setText('Error al eliminar tipo de propiedad')
                mbox.setStandardButtons(
                    QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')

                mbox.exec()
        except Exception as e:
            print("Error en bajaTipoPropiedades (propiedades.py)",e)

    def altaPropiedad(self):
        try:
            propiedad = [var.ui.txtAltaProp.text(), var.ui.txtBajaProp.text(), var.ui.txtDirecionProp.text(),
                         var.ui.cmbProvProp.currentText(), var.ui.cmbMunicipioProp.currentText(), var.ui.txtCpProp.text(),
                         var.ui.cmbTipoProp.text(), var.ui.spinHabitaciones.text(), var.ui.spinBanios.text(),
                         var.ui.txtSuperficie.text(), var.ui.txtPrecioVentaProp.text(), var.ui.txtPrecioAlquilerProp.text(),
                         var.ui.areatxtObservacionesProp.toPlainText(), var.ui.txtPropietarioProp.text(), var.ui.txtMovilProp.text()]

            print(propiedad)
            #comprueba el estado de las checkbox y haz un append
        except Exception as e:
            print("Error en altaPropiedad (propiedades.py)",e)