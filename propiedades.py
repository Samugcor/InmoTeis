from tokenize import String

from PyQt6 import QtWidgets, QtCore
from PyQt6.QtGui import QIcon

import conexion
import conexionserver
import eventos
import propiedades
import var
import venAux

class Propiedades():
    '''def buscarPropiedades(self):
        try:
            #query con parametros de busqueda
        print("aaa")
            #cargar tabla
        except Exception as e:
            print("Error buscando propiedades en la tabla (propiedades.py): "+e)'''

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

            if var.conexionMode:
                if conexion.Conexion.altaTipoPropiedad(tipo):
                    eventos.Eventos.alertMaker("Information","Aviso", "Tipo de propiedad"+tipo+"añadido")

                    eventos.Eventos.cargarTipoPropiedad(self)
                    eventos.Eventos.cargarFiltros(self)
                    var.dlggestion.ui.txtGestTipoProp.setText('')

                else:
                    eventos.Eventos.alertMaker("Critical","Aviso", "Error al añadir tipo de propiedad. Compruebe que el tipo no exista")
            else:
                if conexionserver.ConexionServer.altaTipoPropiedad(tipo):
                    eventos.Eventos.alertMaker("Information", "Aviso", "Tipo de propiedad" + tipo + "añadido")

                    eventos.Eventos.cargarTipoPropiedad(self)
                    eventos.Eventos.cargarFiltros(self)
                    var.dlggestion.ui.txtGestTipoProp.setText('')

                else:
                    eventos.Eventos.alertMaker("Critical", "Aviso","Error al añadir tipo de propiedad. Compruebe que el tipo no exista")

        except Exception as e:
            print("Error en altaTipoPropiedades (propiedades.py)",e)

    def bajaTipoPropiedades(self):
        try:
            tipo = var.dlggestion.ui.txtGestTipoProp.text()
            tipo = tipo.capitalize()
            print(tipo)

            if var.conexionMode:
                if conexion.Conexion.bajaTipoPropiedad(tipo):
                    eventos.Eventos.alertMaker("Information", "Aviso", "Tipo de propiedad" + tipo + "eliminado")

                    eventos.Eventos.cargarTipoPropiedad(self)
                    eventos.Eventos.cargarFiltros(self)
                    var.dlggestion.ui.txtGestTipoProp.setText('')

                else:
                    eventos.Eventos.alertMaker("Critical", "Aviso","Error al eliminar tipo de propiedad. Compruebe que el tipo exista")
            else:
                if conexionserver.ConexionServer.bajaTipoPropiedad(tipo):
                    eventos.Eventos.alertMaker("Information", "Aviso", "Tipo de propiedad" + tipo + "eliminado")
                    eventos.Eventos.cargarTipoPropiedad(self)
                    eventos.Eventos.cargarFiltros(self)
                    var.dlggestion.ui.txtGestTipoProp.setText('')

                else:
                    eventos.Eventos.alertMaker("Critical", "Aviso",
                                               "Error al eliminar tipo de propiedad. Compruebe que el tipo exista")

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

                Propiedades.cargaTablaPropiedades(self,1)
            else:
                QtWidgets.QMessageBox.critical(None, 'Error', 'No se pudo dar de alta a la propiedad en la base de datos.',
                                               QtWidgets.QMessageBox.StandardButton.Cancel)

            #comprueba el estado de las checkbox y haz un append
        except Exception as e:
            print("Error en altaPropiedad (propiedades.py)",e)

    def cargaTablaPropiedades(self,mode):
        try:
            if mode == 1:
                var.npaginapro = 0
            n = 10  # numero de registros por pagina (19) max

            listado = []
            if var.ui.cmbFiltroTipoProp.currentText() != "---" and var.ui.cmbFiltroMuniProp.currentText() != "---":
                #print("Filtros de busqueda ambos")
                listado = conexion.Conexion.listaPropiedadesByTipoMuni(self, var.ui.cmbFiltroTipoProp.currentText(),
                                                                       var.ui.cmbFiltroMuniProp.currentText())
            elif var.ui.cmbFiltroTipoProp.currentText() != "---":
                #print("Filtros de busqueda tipo")
                listado = conexion.Conexion.listaPropiedadesByTipo(self, var.ui.cmbFiltroTipoProp.currentText())
            elif var.ui.cmbFiltroMuniProp.currentText() != "---":
                #print("Filtros de busqueda muni")
                listado = conexion.Conexion.listaPropiedadesByMuni(self, var.ui.cmbFiltroMuniProp.currentText())
            else:
                #print("No filtros de busqueda")
                listado = conexion.Conexion.listadoPropiedades(self)

            #Dividir la lista en sublistas
            listas = [listado[i*n:(i+1)*n] for i in range((len(listado) + n -1) // n)]

            #Activar y desactivar botones
            if var.npaginapro == 0:
                var.ui.btnAnteriorPagProp.setEnabled(False)
            else:
                var.ui.btnAnteriorPagProp.setEnabled(True)

            if var.npaginapro == len(listas)-1:
                var.ui.btnSiguientePagProp.setEnabled(False)
            else:
                var.ui.btnSiguientePagProp.setEnabled(True)

            #Asignar valores
            var.ui.tabPropiedades.clearContents()
            index=0
            for registro in listas[var.npaginapro]:
                #print(registro)
                precioAlquiler="-" if not registro[11] else str(registro[11])
                precioVenta = "-" if not registro[12] else str(registro[12])
                var.ui.tabPropiedades.setRowCount(index+1)
                var.ui.tabPropiedades.setItem(index, 0, QtWidgets.QTableWidgetItem("  "+ str(registro[0]) + "  "))#columna codigo
                var.ui.tabPropiedades.setItem(index, 1, QtWidgets.QTableWidgetItem("  "+ registro[5] + "  "))# clumna municipio
                var.ui.tabPropiedades.setItem(index, 2, QtWidgets.QTableWidgetItem("  "+ registro[7]+ "  "))# clumna tipo prop
                var.ui.tabPropiedades.setItem(index, 3, QtWidgets.QTableWidgetItem("   "+ str(registro[8])+ "   "))# clumna habita
                var.ui.tabPropiedades.setItem(index, 4, QtWidgets.QTableWidgetItem("  "+ str(registro[9])+ "  "))# clumna baños
                var.ui.tabPropiedades.setItem(index, 5, QtWidgets.QTableWidgetItem("  "+ precioAlquiler + " €  "))# clumna precio alquiler
                var.ui.tabPropiedades.setItem(index, 6, QtWidgets.QTableWidgetItem("  "+ precioVenta + " €  "))# clumna precio venta
                var.ui.tabPropiedades.setItem(index, 7, QtWidgets.QTableWidgetItem("  " + registro[16] + "  "))# clumna tipo operacion
                var.ui.tabPropiedades.setItem(index, 8, QtWidgets.QTableWidgetItem("  " + registro[2] + "  "))# clumna fecha de baja

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

            datosTexto=registro[:16]
            datosCheck=registro[16:]

            listado= [var.ui.lblCodigoPropText, var.ui.txtAltaProp, var.ui.txtBajaProp, var.ui.txtDirecionProp,
                         var.ui.cmbProvProp, var.ui.cmbMunicipioProp, var.ui.txtCpProp,
                         var.ui.cmbTipoProp, var.ui.spinHabitaciones, var.ui.spinBanios,
                         var.ui.txtSuperficie, var.ui.txtPrecioAlquilerProp, var.ui.txtPrecioVentaProp,
                         var.ui.areatxtObservacionesProp, var.ui.txtPropietarioProp, var.ui.txtMovilProp]



            for i in range(len(datosTexto)):
                if isinstance(listado[i], QtWidgets.QComboBox):
                    listado[i].setCurrentText(registro[i])
                elif isinstance(listado[i], QtWidgets.QSpinBox):
                    listado[i].setValue(int(registro[i]))
                else:
                    listado[i].setText(registro[i])


            if "Alquiler" in datosCheck[0]:
                var.ui.chkAlquiler.setChecked(True)
            else:
                var.ui.chkAlquiler.setChecked(False)

            if "Venta" in datosCheck[0]:
                var.ui.chkVenta.setChecked(True)
            else:
                var.ui.chkVenta.setChecked(False)

            if "Intercambio" in datosCheck[0]:
                var.ui.chkIntercambio.setChecked(True)
            else:
                var.ui.chkIntercambio.setChecked(False)

            if "Alquilado" in datosCheck[1]:
                var.ui.rbtAlquilado.setChecked(True)
            elif "Vendido" in datosCheck[1]:
                var.ui.rbtVendido.setChecked(True)
            elif "Disponible" in datosCheck[1]:
                var.ui.rbtDisponible.setChecked(True)

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

                propiedades.Propiedades.cargaTablaPropiedades(self,0)
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

                propiedades.Propiedades.cargaTablaPropiedades(self,1)
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

