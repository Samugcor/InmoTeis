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
        if var.conexionMode:
            nuevoCli =[var.ui.txtDniCliente.text(),var.ui.txtAltaCliente.text(),var.ui.txtApellidosCliente.text(),
                    var.ui.txtNombreCliente.text(),var.ui.txtEmailCliente.text(),var.ui.txtMovilCliente.text(),var.ui.txtDirecionCliente.text(),
                    var.ui.cmbProvCli.currentText(),var.ui.cmbMunicipioCli.currentText(), var.ui.txtBajaCliente.text()]
            if nuevoCli[-1]:
                eventos.Eventos.alertMaker("Critical", "Aviso",
                                           "No se puede dar de alta un cliente dado de baja")
                return False
        else:
            nuevoCli = [var.ui.txtDniCliente.text(), var.ui.txtAltaCliente.text(), var.ui.txtApellidosCliente.text(),
                        var.ui.txtNombreCliente.text(), var.ui.txtDirecionCliente.text(), var.ui.txtEmailCliente.text(), var.ui.txtMovilCliente.text(),
                        var.ui.cmbProvCli.currentText(), var.ui.cmbMunicipioCli.currentText()]

        if var.conexionMode:
            if conexion.Conexion.altaCliente(nuevoCli):
                eventos.Eventos.alertMaker("Information","Information","Cliente dado de alta en base de datos")
                Clientes.cargaTablaCientes(self,1)
            else:
                QtWidgets.QMessageBox.critical(None, 'Error', 'No se pudo dar de alta al cliente en la base de datos.',
                                               QtWidgets.QMessageBox.StandardButton.Cancel)
        else:
            print(nuevoCli)
            if conexionserver.ConexionServer.altaCliente(nuevoCli):
                eventos.Eventos.alertMaker("Information","Information","Cliente dado de alta en base de datos")
                Clientes.cargaTablaCientes(self,1)
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


    def cargaTablaCientes(self,mode):
        try:
            if mode==1:
                var.npaginacli=0

            n=10 #numero de registros por pagina (19) max

            if var.conexionMode:
                listado= conexion.Conexion.listadoClientes(self)
            else:
                listado = conexionserver.ConexionServer.listadoClientes(self)

            '''
            my_list = [1, 2, 3, 4, 5,
              6, 7, 8, 9]

            # How many elements each
            # list should have
            n = 4 
            
            # using list comprehension
            final = [my_list[i * n:(i + 1) * n] for i in range((len(my_list) + n - 1) // n )] 
            print (final)
            '''
            listas = [listado[i*n:(i+1)*n] for i in range((len(listado) + n -1) // n)]

            #Control botones
            if var.npaginacli == 0:
                var.ui.btnAnteriorPagCli.setEnabled(False)
            else:
                var.ui.btnAnteriorPagCli.setEnabled(True)

            if var.npaginacli == len(listas)-1:
                var.ui.btnSiguientePagCli.setEnabled(False)
            else:
                var.ui.btnSiguientePagCli.setEnabled(True)


            #Asignar valores
            var.ui.tabClientes.clearContents()
            index=0
            for registro in listas[var.npaginacli]:
                var.ui.tabClientes.setRowCount(index+1)
                var.ui.tabClientes.setItem(index, 0, QtWidgets.QTableWidgetItem("  "+ registro[0] + "  "))#dni
                var.ui.tabClientes.setItem(index, 1, QtWidgets.QTableWidgetItem("  "+ registro[2] + "  "))#apellido
                var.ui.tabClientes.setItem(index, 2, QtWidgets.QTableWidgetItem("  "+ registro[3]+ "  "))#nombre

                if var.conexionMode:
                    var.ui.tabClientes.setItem(index, 3, QtWidgets.QTableWidgetItem("   "+ registro[5]+ "   "))#movil
                else:
                    var.ui.tabClientes.setItem(index, 3, QtWidgets.QTableWidgetItem("   "+ registro[6]+ "   "))

                var.ui.tabClientes.setItem(index, 4, QtWidgets.QTableWidgetItem("  "+ registro[7]+ "  "))#provincia
                var.ui.tabClientes.setItem(index, 5, QtWidgets.QTableWidgetItem("  "+ registro[8]+ "  "))#municipio
                registro[9] = " " if registro[9] is None else registro[9]
                var.ui.tabClientes.setItem(index, 6, QtWidgets.QTableWidgetItem("  "+ registro[9]+ "  "))#baja



                var.ui.tabClientes.item(index, 0).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                var.ui.tabClientes.item(index, 1).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                var.ui.tabClientes.item(index, 2).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                var.ui.tabClientes.item(index, 3).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                var.ui.tabClientes.item(index, 4).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                var.ui.tabClientes.item(index, 5).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                var.ui.tabClientes.item(index, 6).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

                index+=1


        except Exception as error:
            print("Error cargando la tabla de clientes (clientes.py)", error)

    def cargaOneCliente(self):
        try:
            fila=var.ui.tabClientes.selectedItems()
            datos=[dato.text() for dato in fila]

            if var.conexionMode:
                registro=conexion.Conexion.datosOneCliente(str(datos[0]))
            else:
                registro=conexionserver.ConexionServer.datosOneCliente(str(datos[0]))

            if var.conexionMode:
                listado= [var.ui.txtDniCliente,var.ui.txtAltaCliente,var.ui.txtApellidosCliente,
                    var.ui.txtNombreCliente,var.ui.txtEmailCliente,var.ui.txtMovilCliente,var.ui.txtDirecionCliente,
                    var.ui.cmbProvCli,var.ui.cmbMunicipioCli, var.ui.txtBajaCliente]
            else:
                #
                listado = [var.ui.txtDniCliente, var.ui.txtAltaCliente, var.ui.txtApellidosCliente,
                           var.ui.txtNombreCliente, var.ui.txtEmailCliente, var.ui.txtDirecionCliente,
                           var.ui.txtMovilCliente, var.ui.cmbProvCli, var.ui.cmbMunicipioCli, var.ui.txtBajaCliente]

            #print(registro)
            #print(listado)
            for i in range(len(listado)):
                registro[i] = " " if registro[i] == "None" else registro[i]
                if isinstance(listado[i], QtWidgets.QComboBox):
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


            if not modifCli[0]:
                eventos.Eventos.alertMaker("Critical", "Aviso","No se ha seleccionado ningún cliente que modificar")
                return
            if not eventos.Eventos.validarFechaAlta():
                return

            if var.conexionMode:
                if conexion.Conexion.modifCliente(modifCli):
                    eventos.Eventos.alertMaker("Information", "Aviso","Datos de cliente modificado")

                    clientes.Clientes.cargaTablaCientes(self,0)
                else:
                    eventos.Eventos.alertMaker("Critical", "Aviso","Error al modificar datos de cliente")
            else:
                if conexionserver.ConexionServer.modifCliente(modifCli):
                    eventos.Eventos.alertMaker("Information", "Aviso", "Datos de cliente modificado")

                    clientes.Clientes.cargaTablaCientes(self,0)
                else:
                    eventos.Eventos.alertMaker("Critical", "Aviso", "Error al modificar datos de cliente")

        except Exception as error:
            print("Error modificando la tabla de clientes (clientes.py): ", error)

    def bajaCliente(self):
        try:
            if not eventos.Eventos.validarFechaBaja():
                return
            print("fecha comprobada")

            datos= [var.ui.txtDniCliente.text(),var.ui.txtBajaCliente.text()]

            if var.conexionMode:
                if conexion.Conexion.bajaCliente(datos):
                    eventos.Eventos.alertMaker("Information", "Aviso", "Cliente dado de baja")

                    clientes.Clientes.cargaTablaCientes(self,1)
                else:
                    eventos.Eventos.alertMaker("Critical", "Aviso", "Error Baja Cliente: cliente no existe o ya ha sido dado de baja")
            else:
                if conexionserver.ConexionServer.bajaCliente(datos):
                    eventos.Eventos.alertMaker("Information", "Aviso", "Cliente dado de baja")

                    clientes.Clientes.cargaTablaCientes(self,1)
                else:
                    eventos.Eventos.alertMaker("Critical", "Aviso",
                                               "Error Baja Cliente: cliente no existe o ya ha sido dado de baja")

        except Exception as e:
            print("Error baja de clientes", e)

    def buscarCliente(self):
        dni=var.ui.txtDniCliente.text()
        if dni == "":
            mbox = QtWidgets.QMessageBox()
            mbox.setWindowIcon(QIcon('./img/house.svg'))
            mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
            mbox.setWindowTitle('Aviso')
            mbox.setText('No puedes buscar clientes sin un DNI')
            mbox.setStandardButtons(
                QtWidgets.QMessageBox.StandardButton.Ok)
            mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
            mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')

            mbox.exec()

        elif eventos.Eventos.validarDNIcli(dni) == True:
            if var.conexionMode:
                registro = conexion.Conexion.datosOneCliente(dni)
            else:
                registro = conexionserver.ConexionServer.datosOneCliente(dni)

            if registro:
                listado = [var.ui.txtDniCliente, var.ui.txtAltaCliente, var.ui.txtApellidosCliente,
                           var.ui.txtNombreCliente, var.ui.txtEmailCliente, var.ui.txtMovilCliente,
                           var.ui.txtDirecionCliente,
                           var.ui.cmbProvCli, var.ui.cmbMunicipioCli, var.ui.txtBajaCliente]

                for i in range(len(listado)):
                    if i == 7 or i == 8:
                        listado[i].setCurrentText(registro[i])
                    else:
                        listado[i].setText(registro[i])
            else:
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowIcon(QIcon('./img/house.svg'))
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
                mbox.setWindowTitle('Aviso')
                mbox.setText('No se ha encontrado un cliente con el DNI ' + dni)
                mbox.setStandardButtons(
                    QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')

                mbox.exec()
        else:
            #Nunca se usa porque el campo no borra el contenido si detecta que el formato no es valido
            mbox = QtWidgets.QMessageBox()
            mbox.setWindowIcon(QIcon('./img/house.svg'))
            mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
            mbox.setWindowTitle('Aviso')
            mbox.setText('El DNI no es valido')
            mbox.setStandardButtons(
                QtWidgets.QMessageBox.StandardButton.Ok)
            mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
            mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')

            mbox.exec()

