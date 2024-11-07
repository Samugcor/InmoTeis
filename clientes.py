from tabnanny import check

from PyQt6 import QtWidgets, QtCore
from PyQt6.QtGui import QIcon

import clientes
import conexion
import conexionserver
import eventos
import var

class Clientes:
    def checkDNI(dni):
        try:
            dni = str(dni).upper()
            var.ui.txtDniCliente.setText(str(dni))
            check= eventos.Eventos.validarDNIcli(dni)

            if check:
                var.ui.txtDniCliente.setStyleSheet("background-color: rgb(255, 255, 220);")
            else:
                var.ui.txtDniCliente.setStyleSheet('background-color:#FFC0CB;')  # y si no un aspa en color rojo
                var.ui.txtDniCliente.setText(None)
                var.ui.txtDniCliente.setFocus()
        except Exception as e:
            print("Error check clientes",e)

    def altaClientes(self):
        nuevoCli =[var.ui.txtDniCliente.text(),var.ui.txtAltaCliente.text(),var.ui.txtApellidosCliente.text(),
                var.ui.txtNombreCliente.text(),var.ui.txtEmailCliente.text(),var.ui.txtMovilCliente.text(),var.ui.txtDirecionCliente.text(),
                var.ui.cmbProvCli.currentText(),var.ui.cmbMunicipioCli.currentText(), var.ui.txtBajaCliente.text()]

        if conexion.Conexion.altaCliente(nuevoCli):
            mbox = QtWidgets.QMessageBox()
            mbox.setWindowIcon(QIcon('./img/house.svg'))
            mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
            mbox.setWindowTitle('Aviso')
            mbox.setText('Cliente dado de alta en base de datos')
            mbox.setStandardButtons(
                QtWidgets.QMessageBox.StandardButton.Ok)
            mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
            mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')

            mbox.exec()

            Clientes.cargaTablaCientes(self)
        else:
            QtWidgets.QMessageBox.critical(None, 'Error', 'No se pudo dar de alta al cliente en la base de datos.',
                                           QtWidgets.QMessageBox.StandardButton.Cancel)

    @staticmethod
    def checkEmail():
        try:
            mail = str(var.ui.txtEmailCliente.text())
            if eventos.Eventos.validarMail(mail):
                var.ui.txtEmailCliente.setStyleSheet('background-color: rgb(255, 255, 255);')
                var.ui.txtEmailCliente.setText(mail.lower())

            else:
                var.ui.txtEmailCliente.setStyleSheet('background-color:#FFC0CB; font-style: italic;')
                var.ui.txtEmailCliente.setText(None)
                var.ui.txtEmailCliente.setText("correo no válido")
                var.ui.txtEmailCliente.setFocus()

        except Exception as error:
            print("Erros checkeando el email", error)

    @staticmethod
    def checkMovil():
        try:
            movil = str(var.ui.txtMovilCliente.text())
            if eventos.Eventos.validarMovil(movil):
                var.ui.txtMovilCliente.setStyleSheet('background-color: rgb(255, 255, 255);')
                var.ui.txtMovilCliente.setText(movil.lower())

            else:
                var.ui.txtMovilCliente.setStyleSheet('background-color:#FFC0CB;')
                var.ui.txtMovilCliente.setText(None)
                var.ui.txtMovilCliente.setFocus()

        except Exception as error:
            print("Erros checkeando el movil", error)

    def cargaTablaCientes(self):
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

    def cargaOneCliente(self):
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

    def modifCliente(self):
        try:
            modifCli = [var.ui.txtDniCliente.text(), var.ui.txtAltaCliente.text(), var.ui.txtApellidosCliente.text(),
                        var.ui.txtNombreCliente.text(), var.ui.txtEmailCliente.text(), var.ui.txtMovilCliente.text(),
                        var.ui.txtDirecionCliente.text(), var.ui.cmbProvCli.currentText(), var.ui.cmbMunicipioCli.currentText(),
                        var.ui.txtBajaCliente.text()]

            if conexion.Conexion.modifCliente(modifCli):
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowIcon(QIcon('./img/house.svg'))
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setWindowTitle('Aviso')
                mbox.setText('Datos de cliente modificados')
                mbox.setStandardButtons(
                    QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')

                mbox.exec()

                clientes.Clientes.cargaTablaCientes(self)
            else:
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowIcon(QIcon('./img/house.svg'))
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
                mbox.setWindowTitle('Aviso')
                mbox.setText('Error al modificar datos de cliente')
                mbox.setStandardButtons(
                    QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')

                mbox.exec()

        except Exception as error:
            print("Error modificando la tabla de clientes (clientes.py): ", error)

    def bajaCliente(self):
        try:
            datos= [var.ui.txtDniCliente.text(),var.ui.txtBajaCliente.text()]

            if conexion.Conexion.bajaCliente(datos):
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowIcon(QIcon('./img/house.svg'))
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setWindowTitle('Aviso')
                mbox.setText('Cliente dado de baja')
                mbox.setStandardButtons(
                    QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')

                mbox.exec()

                clientes.Clientes.cargaTablaCientes(self)
            else:
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowIcon(QIcon('./img/house.svg'))
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
                mbox.setWindowTitle('Aviso')
                mbox.setText('Error Baja Cliente: cliente no existe o ya ha sido dado de baja')
                mbox.setStandardButtons(
                    QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')

                mbox.exec()

        except Exception as e:
            print("Error baja de clientes", e)
