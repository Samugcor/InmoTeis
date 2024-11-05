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
                         var.ui.cmbTipoProp.currentText(), var.ui.spinHabitaciones.text(), var.ui.spinBanios.text(),
                         var.ui.txtSuperficie.text(), var.ui.txtPrecioAlquilerProp.text(), var.ui.txtPrecioVentaProp.text(),
                         var.ui.areatxtObservacionesProp.toPlainText(), var.ui.txtPropietarioProp.text(), var.ui.txtMovilProp.text()]

            tipoOp = ""
            if var.ui.chkAlquiler.isChecked():
                tipoOp = "Alquiler" if len(tipoOp) == 0 else tipoOp+" - Alquiler"
            if var.ui.chkVenta.isChecked():
                tipoOp = "Venta" if len(tipoOp) == 0 else tipoOp+" - Venta"
            if var.ui.chkIntercambio.isChecked():
                tipoOp = "Intercambio" if len(tipoOp) == 0 else tipoOp+" - Intercambio"

            propiedad.append(tipoOp)

            if var.ui.rgEstado.checkedId() == 1:
                propiedad.append("Alquilado")
            elif var.ui.rgEstado.checkedId() == 2:
                propiedad.append("Vendido")
            else:
                propiedad.append("Disponible")

            print(propiedad)

            if conexion.Conexion.altaPropiedad(propiedad):
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowIcon(QIcon('./img/house.svg'))
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setWindowTitle('Aviso')
                mbox.setText('Propiedad dada de alta en base de datos')
                mbox.setStandardButtons(
                    QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')

                mbox.exec()

                #Clientes.cargaTablaCientes(self)
            else:
                QtWidgets.QMessageBox.critical(None, 'Error', 'No se pudo dar de alta a la propiedad en la base de datos.',
                                               QtWidgets.QMessageBox.StandardButton.Cancel)

            #comprueba el estado de las checkbox y haz un append
        except Exception as e:
            print("Error en altaPropiedad (propiedades.py)",e)

    def cargaTablaPropiedades(self):
        try:
            listado= conexion.Conexion.listadoClientes(self)
            #listado = conexionserver.ConexionServer.listadoClientes(self)
            index=0
            for registro in listado:
                var.ui.tabClientes.setRowCount(index+1)
                var.ui.tabClientes.setItem(index, 0, QtWidgets.QTableWidgetItem("  "+ registro[0] + "  "))
                var.ui.tabClientes.setItem(index, 1, QtWidgets.QTableWidgetItem("  "+ registro[2] + "  "))
                var.ui.tabClientes.setItem(index, 2, QtWidgets.QTableWidgetItem("  "+ registro[3]+ "  "))
                var.ui.tabClientes.setItem(index, 3, QtWidgets.QTableWidgetItem("   "+ registro[5]+ "   "))
                var.ui.tabClientes.setItem(index, 4, QtWidgets.QTableWidgetItem("  "+ registro[7]+ "  "))
                var.ui.tabClientes.setItem(index, 5, QtWidgets.QTableWidgetItem("  "+ registro[8]+ "  "))
                var.ui.tabClientes.setItem(index, 6, QtWidgets.QTableWidgetItem("  "+ registro[9]+ "  "))

                var.ui.tabClientes.item(index, 0).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                var.ui.tabClientes.item(index, 1).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                var.ui.tabClientes.item(index, 2).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                var.ui.tabClientes.item(index, 3).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                var.ui.tabClientes.item(index, 4).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                var.ui.tabClientes.item(index, 5).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                var.ui.tabClientes.item(index, 6).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

                index+=1


        except Exception as error:
            print("Error cargando la tabla de clientes", error)

    def cargaOnePropiedad(self):
        try:
            fila=var.ui.tabClientes.selectedItems()
            datos=[dato.text() for dato in fila]
            registro=conexion.Conexion.datosOneCliente(str(datos[0]))
            listado= [var.ui.txtDniCliente,var.ui.txtAltaCliente,var.ui.txtApellidosCliente,
                var.ui.txtNombreCliente,var.ui.txtEmailCliente,var.ui.txtMovilCliente,var.ui.txtDirecionCliente,
                var.ui.cmbProvCli,var.ui.cmbMunicipioCli, var.ui.txtBajaCliente]

            #print(registro)
            #print(listado)
            for i in range(len(listado)):
                if i==7 or i==8:
                    listado[i].setCurrentText(registro[i])
                else:
                    listado[i].setText(registro[i])

        except Exception as error:
            print("Error cargando datos del cliente", error)


'''
codigo, altaprop, bajaprop, dirprop, provprop, muniprop, cpprop,
tipoprop, habprop, banprop, superprop, prealquiprop, prevenprop,
obserprop, tipooperprop, estadoprop, nomeprop, movilprop
	'''