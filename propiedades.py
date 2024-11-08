from tokenize import String

from PyQt6 import QtWidgets, QtCore
from PyQt6.QtGui import QIcon

import conexion
import eventos
import propiedades
import var
import venAux

class Propiedades():
    def formPropiedad(self):
        try:
            #BAJA PROP
            if var.ui.txtBajaProp.text() == "":
                var.ui.rbtDisponible.setEnabled(True)
                var.ui.rbtVendido.setEnabled(False)
                var.ui.rbtAlquilado.setEnabled(False)
                var.ui.rbtDisponible.setChecked(True)
            else:
                var.ui.rbtDisponible.setEnabled(False)
                var.ui.rbtVendido.setEnabled(True)
                var.ui.rbtAlquilado.setEnabled(True)
                var.ui.rbtVendido.setChecked(True)

            ##PRECIO VENTA
            if var.ui.txtPrecioVentaProp.text() == "":
                var.ui.chkVenta.setChecked(False)
                var.ui.chkVenta.setEnabled(False)
            else:
                var.ui.chkVenta.setChecked(True)
                var.ui.chkVenta.setEnabled(True)

            ##PRECIO ALQUILER
            if var.ui.txtPrecioAlquilerProp.text() == "":
                var.ui.chkAlquiler.setChecked(False)
                var.ui.chkAlquiler.setEnabled(False)
            else:
                var.ui.chkAlquiler.setChecked(True)
                var.ui.chkAlquiler.setEnabled(True)

        except Exception as e:
            print("ErRoR cargando la interfaz del formulario de propiedades (propiedades.py): ",e)

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

                Propiedades.cargaTablaPropiedades(self)
            else:
                QtWidgets.QMessageBox.critical(None, 'Error', 'No se pudo dar de alta a la propiedad en la base de datos.',
                                               QtWidgets.QMessageBox.StandardButton.Cancel)

            #comprueba el estado de las checkbox y haz un append
        except Exception as e:
            print("Error en altaPropiedad (propiedades.py)",e)

    def cargaTablaPropiedades(self):
        try:
            listado= conexion.Conexion.listadoPropiedades(self)
            index=0
            for registro in listado:
                #print(registro)
                precioAlquiler="-" if not registro[11] else str(registro[11])
                precioVenta = "-" if not registro[12] else str(registro[12])
                var.ui.tabPropiedades.setRowCount(index+1)
                var.ui.tabPropiedades.setItem(index, 0, QtWidgets.QTableWidgetItem("  "+ str(registro[0]) + "  "))
                var.ui.tabPropiedades.setItem(index, 1, QtWidgets.QTableWidgetItem("  "+ registro[5] + "  "))
                var.ui.tabPropiedades.setItem(index, 2, QtWidgets.QTableWidgetItem("  "+ registro[7]+ "  "))
                var.ui.tabPropiedades.setItem(index, 3, QtWidgets.QTableWidgetItem("   "+ str(registro[8])+ "   "))
                var.ui.tabPropiedades.setItem(index, 4, QtWidgets.QTableWidgetItem("  "+ str(registro[9])+ "  "))
                var.ui.tabPropiedades.setItem(index, 5, QtWidgets.QTableWidgetItem("  "+ precioAlquiler + " €  "))
                var.ui.tabPropiedades.setItem(index, 6, QtWidgets.QTableWidgetItem("  "+ precioVenta + " €  "))
                var.ui.tabPropiedades.setItem(index, 7, QtWidgets.QTableWidgetItem("  " + registro[14] + "  "))
                var.ui.tabPropiedades.setItem(index, 8, QtWidgets.QTableWidgetItem("  " + registro[2] + "  "))

                var.ui.tabPropiedades.item(index, 0).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                var.ui.tabPropiedades.item(index, 1).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                var.ui.tabPropiedades.item(index, 2).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                var.ui.tabPropiedades.item(index, 3).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                var.ui.tabPropiedades.item(index, 4).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                var.ui.tabPropiedades.item(index, 5).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter)
                var.ui.tabPropiedades.item(index, 6).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter)
                var.ui.tabPropiedades.item(index, 7).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                var.ui.tabPropiedades.item(index, 8).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

                index+=1


        except Exception as error:
            print("Error cargando la tabla de propiedades (propiedades.py", error)

    def cargaOnePropiedad(self):
        try:
            var.ui.chkAlquiler.setChecked(False)
            var.ui.chkVenta.setChecked(False)
            var.ui.chkIntercambio.setChecked(False)

            fila=var.ui.tabPropiedades.selectedItems()
            datos=[dato.text() for dato in fila]

            registro=conexion.Conexion.datosOnePropiedad(str(datos[0]))

            listado= [var.ui.lblCodigoPropText, var.ui.txtAltaProp, var.ui.txtBajaProp, var.ui.txtDirecionProp,
                         var.ui.cmbProvProp, var.ui.cmbMunicipioProp, var.ui.txtCpProp,
                         var.ui.cmbTipoProp, var.ui.spinHabitaciones, var.ui.spinBanios,
                         var.ui.txtSuperficie, var.ui.txtPrecioAlquilerProp, var.ui.txtPrecioVentaProp,
                         var.ui.areatxtObservacionesProp,"placeholder","placeholder", var.ui.txtPropietarioProp, var.ui.txtMovilProp]



            for i in range(len(registro)):
                if i in (4,5,7):
                    listado[i].setCurrentText(registro[i])
                elif i in (8,9):
                    listado[i].setValue(int(registro[i]))
                elif i == 14:
                    if "Alquiler" in registro[i]:
                        var.ui.chkAlquiler.setChecked(True)
                    if "Venta" in registro[i]:
                        var.ui.chkVenta.setChecked(True)
                    if "Intercambio" in registro[i]:
                        var.ui.chkIntercambio.setChecked(True)
                elif i == 15:
                    if "Alquilado" in registro[i]:
                        var.ui.rbtAlquilado.setChecked(True)
                    elif "Vendido" in registro[i]:
                        var.ui.rbtVendido.setChecked(True)
                    elif "Disponible" in registro[i]:
                        var.ui.rbtDisponible.setChecked(True)
                else:
                    listado[i].setText(registro[i])

        except Exception as error:
            print("Error cargando datos de propiedad (propiedades.py)", error)

    def modifPropiedad(self):
        try:
            modifProp = [var.ui.lblCodigoPropText.text(), var.ui.txtAltaProp.text(), var.ui.txtBajaProp.text(), var.ui.txtDirecionProp.text(),
                         var.ui.cmbProvProp.currentText(), var.ui.cmbMunicipioProp.currentText(), var.ui.txtCpProp.text(),
                         var.ui.cmbTipoProp.currentText(), var.ui.spinHabitaciones.text(), var.ui.spinBanios.text(),
                         var.ui.txtSuperficie.text(), var.ui.txtPrecioAlquilerProp.text(), var.ui.txtPrecioVentaProp.text(),
                         var.ui.areatxtObservacionesProp.toPlainText(), var.ui.txtPropietarioProp.text(), var.ui.txtMovilProp.text()]
            tipoOp = ""
            if var.ui.chkAlquiler.isChecked():
                tipoOp = "Alquiler" if len(tipoOp) == 0 else tipoOp + " - Alquiler"
            if var.ui.chkVenta.isChecked():
                tipoOp = "Venta" if len(tipoOp) == 0 else tipoOp + " - Venta"
            if var.ui.chkIntercambio.isChecked():
                tipoOp = "Intercambio" if len(tipoOp) == 0 else tipoOp + " - Intercambio"

            modifProp.append(tipoOp)

            if var.ui.rgEstado.checkedId() == 1:
                modifProp.append("Alquilado")
            elif var.ui.rgEstado.checkedId() == 2:
                modifProp.append("Vendido")
            else:
                modifProp.append("Disponible")

            if conexion.Conexion.modifPropiedad(modifProp):
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowIcon(QIcon('./img/house.svg'))
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setWindowTitle('Aviso')
                mbox.setText('Datos de propiedad modificados')
                mbox.setStandardButtons(
                    QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')

                mbox.exec()

                propiedades.Propiedades.cargaTablaPropiedades(self)
            else:
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowIcon(QIcon('./img/house.svg'))
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
                mbox.setWindowTitle('Aviso')
                mbox.setText('Error al modificar datos de propiedad')
                mbox.setStandardButtons(
                    QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')

                mbox.exec()

        except Exception as error:
            print("Error modificando la tabla de propiedades (propiedades.py)", error)

    def bajaPropiedad(self):
        try:
            datos= [var.ui.lblCodigoPropText.text(),var.ui.txtBajaProp.text()]

            if conexion.Conexion.bajaPropiedad(datos):
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowIcon(QIcon('./img/house.svg'))
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setWindowTitle('Aviso')
                mbox.setText('Propiedad dada de baja')
                mbox.setStandardButtons(
                    QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')

                mbox.exec()

                propiedades.Propiedades.cargaTablaPropiedades(self)
            else:
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowIcon(QIcon('./img/house.svg'))
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
                mbox.setWindowTitle('Aviso')
                mbox.setText('Error Baja Propiedad: propiedad no existe o ya ha sido dado de baja')
                mbox.setStandardButtons(
                    QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')

                mbox.exec()

        except Exception as e:
            print("Error baja de propiedad (propiedades.py): ", e)