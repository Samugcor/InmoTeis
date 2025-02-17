from PyQt6 import QtWidgets, QtCore
from PyQt6.QtGui import QIcon

import conexion
import eventos
import var
import vendedor

class Vendedor:
    def checkDNI(dni):
        try:
            dni = str(dni).upper()
            var.ui.txtDniVendedor.setText(str(dni))
            check= eventos.Eventos.validarDNIcli(dni)

            if check:
                var.ui.txtDniVendedor.setStyleSheet("background-color: rgb(255, 255, 220);")
            else:
                var.ui.txtDniVendedor.setStyleSheet('background-color:#FFC0CB;')  # y si no un aspa en color rojo
                var.ui.txtDniVendedor.setText(None)
                var.ui.txtDniVendedor.setFocus()
        except Exception as e:
            print("Error check dni vendedor",e)

    @staticmethod
    def checkEmail():
        try:
            mail = str(var.ui.txtEmailVendedor.text())
            if eventos.Eventos.validarMail(mail):
                var.ui.txtEmailVendedor.setStyleSheet('background-color: rgb(255, 255, 255);')
                var.ui.txtEmailVendedor.setText(mail.lower())

            else:
                var.ui.txtEmailVendedor.setStyleSheet('background-color:#FFC0CB; font-style: italic;')
                var.ui.txtEmailVendedor.setText(None)
                var.ui.txtEmailVendedor.setFocus()

        except Exception as error:
            print("Erros checkeando el email vendedor", error)

    @staticmethod
    def checkMovil():
        try:
            movil = str(var.ui.txtMovilVendedor.text())
            if eventos.Eventos.validarMovil(movil):
                var.ui.txtMovilVendedor.setStyleSheet('background-color: rgb(255, 255, 255);')
                var.ui.txtMovilVendedor.setText(movil.lower())

            else:
                var.ui.txtMovilVendedor.setStyleSheet('background-color:#FFC0CB;')
                var.ui.txtMovilVendedor.setText(None)
                var.ui.txtMovilVendedor.setFocus()

        except Exception as error:
            print("Erros checkeando el movil vendedor", error)

    def cargaTablaVendedores(self):
        try:

            listado = conexion.Conexion.listadoVendedores(self)


            if len(listado) == 0:
                var.ui.tabVendedores.clearContents()
                var.ui.tabVendedores.setRowCount(1)
                var.ui.tabVendedores.setItem(0, 0, QtWidgets.QTableWidgetItem("No se encontraron registros"))
                var.ui.tabVendedores.setSpan(0, 0, 1, var.ui.tabVendedores.columnCount())  # Span all columns
                var.ui.tabVendedores.item(0, 0).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                return
            else:
                var.ui.tabVendedores.setSpan(0, 0, 1, 1)  # Span all columns



            # Asignar valores
            var.ui.tabVendedores.clearContents()
            index = 0
            for registro in listado:
                var.ui.tabVendedores.setRowCount(index + 1)
                var.ui.tabVendedores.setItem(index, 0, QtWidgets.QTableWidgetItem("  " + str(registro[0]) + "  "))  # id
                var.ui.tabVendedores.setItem(index, 1, QtWidgets.QTableWidgetItem("  " + registro[2] + "  "))  # nombre
                var.ui.tabVendedores.setItem(index, 2, QtWidgets.QTableWidgetItem("  " + registro[5] + "  "))  # movil
                var.ui.tabVendedores.setItem(index, 3, QtWidgets.QTableWidgetItem("   " + registro[7] + "   "))  # delegacion


                var.ui.tabVendedores.item(index, 0).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                var.ui.tabVendedores.item(index, 1).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                var.ui.tabVendedores.item(index, 2).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                var.ui.tabVendedores.item(index, 3).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

                index += 1


        except Exception as error:
            print("Error cargando la tabla de vendedores (vendedores.py)", error)

    def altaVendedores(self):
        try:
            nuevoVendedor =[var.ui.txtDniVendedor.text(), var.ui.txtNombreVendedor.text(), var.ui.txtAltaVendedor.text(), var.ui.txtBajaVendedor.text(),
                    var.ui.txtMovilVendedor.text(),var.ui.txtEmailVendedor.text(),var.ui.cmbProvVendedor.currentText()]

            if nuevoVendedor[3]:
                eventos.Eventos.alertMaker("Critical", "Aviso",
                                           "No se puede dar de alta un vendedor dado de baja")
                return
            if not nuevoVendedor[0] or not nuevoVendedor[1] or not nuevoVendedor[4] or not nuevoVendedor[6]:
                eventos.Eventos.alertMaker("Critical", "Aviso",
                                           "Falta informacion en campos obligatorios")
                return
            if nuevoVendedor[0] in conexion.Conexion.getAllDniVendedores(self):
                eventos.Eventos.alertMaker("Critical", "Aviso",
                                           "DNI ya existente")
                return


            if conexion.Conexion.altaVendedores(nuevoVendedor):
                eventos.Eventos.alertMaker("Information","Information","Vendedor dado de alta en base de datos")
                Vendedor.cargaTablaVendedores(self)
            else:
                QtWidgets.QMessageBox.critical(None, 'Error', 'No se pudo dar de alta al vendedor en la base de datos.',
                                               QtWidgets.QMessageBox.StandardButton.Cancel)
        except Exception as error:
            print("Error cargando la tabla de vendedores", error)

    def cargaOneVendedor(self):
        try:
            fila=var.ui.tabVendedores.selectedItems()
            datos=[dato.text() for dato in fila]

            registro=conexion.Conexion.datosOneVendedor(str(datos[0]))

            listado= [var.ui.lblIDVendedor, var.ui.txtDniVendedor, var.ui.txtNombreVendedor,
                      var.ui.txtAltaVendedor, var.ui.txtBajaVendedor,
                    var.ui.txtMovilVendedor,var.ui.txtEmailVendedor,
                      var.ui.cmbProvVendedor]

            #print(registro)
            #print(listado)
            for i in range(len(listado)):

                if isinstance(listado[i], QtWidgets.QComboBox):
                    listado[i].setCurrentText(registro[i])
                else:
                    listado[i].setText(registro[i])

        except Exception as error:
            print("Error cargando datos del vendedor", error)

    def modifVendedor(self):
        try:
            modifVendedor = [var.ui.lblIDVendedor.text(), var.ui.txtDniVendedor.text(), var.ui.txtNombreVendedor.text(), var.ui.txtAltaVendedor.text(), var.ui.txtBajaVendedor.text(),
                    var.ui.txtMovilVendedor.text(),var.ui.txtEmailVendedor.text(),var.ui.cmbProvVendedor.currentText()]


            if not modifVendedor[0]:
                eventos.Eventos.alertMaker("Critical", "Aviso","No se ha seleccionado ningún vendedor que modificar")
                return


            if conexion.Conexion.modifVendedor(modifVendedor):
                eventos.Eventos.alertMaker("Information", "Aviso","Datos de vendedor modificado")
                vendedor.Vendedor.cargaTablaVendedores(self)
            else:
                eventos.Eventos.alertMaker("Critical", "Aviso","Error al modificar datos de vendedor")

        except Exception as error:
            print("Error modificando la tabla de vendedores (vendedor.py): ", error)

    def bajaVendedor(self):
        try:
            if var.ui.txtBajaVendedor.text():
                eventos.Eventos.alertMaker("Critical", "Aviso",
                                           "Error Baja Vendedor: el vendedor ya está dado de baja")
                return
            idVendedor= var.ui.lblIDVendedor.text()

            if conexion.Conexion.bajaVendedor(idVendedor):
                eventos.Eventos.alertMaker("Information", "Aviso", "Vendedor dado de baja")
                vendedor.Vendedor.cargaTablaVendedores(self)
            else:
                eventos.Eventos.alertMaker("Critical", "Aviso", "Error Baja Vendedor: vendedor no existe o ya ha sido dado de baja")

        except Exception as e:
            print("Error baja de vendedor", e)

    def buscarVendedor(self):
        try:
            movil=var.ui.txtMovilVendedor.text()
            if movil == "":
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowIcon(QIcon('./img/house.svg'))
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
                mbox.setWindowTitle('Aviso')
                mbox.setText('No puedes buscar vendedores sin un movil')
                mbox.setStandardButtons(
                    QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')

                mbox.exec()
                return


            registro = conexion.Conexion.datosVendedorByMovil(movil)

            listado = [var.ui.lblIDVendedor, var.ui.txtDniVendedor, var.ui.txtNombreVendedor,
                       var.ui.txtAltaVendedor, var.ui.txtBajaVendedor,
                       var.ui.txtMovilVendedor, var.ui.txtEmailVendedor,
                       var.ui.cmbProvVendedor]

            # print(registro)
            # print(listado)
            for i in range(len(listado)):
                registro[i] = " " if registro[i] == "None" else registro[i]
                if isinstance(listado[i], QtWidgets.QComboBox):
                    listado[i].setCurrentText(registro[i])
                else:
                    listado[i].setText(registro[i])

        except Exception as error:
            print("Error cargando datos de vendedor", error)


