from operator import index

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QPushButton, QHBoxLayout, QWidget
from PyQt6 import QtWidgets, QtCore

import conexion
import eventos
import propiedades
import var

class Ventas:
    @staticmethod
    def guardarFactura ():
        try:
            var.ui.btn_GuardarFactura.clearFocus()
            nuevaFactura = [var.ui.txt_FechaFactura.text().strip(),var.ui.txt_DNIFactura.text().strip()]
            if conexion.Conexion.altaFactura(nuevaFactura):
                eventos.Eventos.alertMaker("Information","Information","Factura guardada en la base de datos")
                Ventas.cargarTablaFacturas()
            else:
                QtWidgets.QMessageBox.critical('Error', 'Error', 'No se pudo guardar la factura en la base de datos.',
                                               QtWidgets.QMessageBox.StandardButton.Cancel)

        except Exception as e:
            print("Error guardando factura (ventas.py): ",e)

    @staticmethod
    def cargarTablaFacturas():
        try:
            listaFacturas = conexion.Conexion.listaFacturas()

            if len(listaFacturas) == 0:
                var.ui.tbl_facturas.clearContents()
                var.ui.tbl_facturas.setRowCount(1)
                var.ui.tbl_facturas.setItem(0, 0, QtWidgets.QTableWidgetItem("No se encontraron facturas"))
                var.ui.tbl_facturas.setSpan(0, 0, 1, var.ui.tbl_facturas.columnCount())  # Span all columns
                var.ui.tbl_facturas.item(0, 0).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                return
            else:
                var.ui.tbl_facturas.setSpan(0, 0, 1, 1)  # Span all columns


            var.ui.tbl_facturas.clearContents()
            index=0
            for factura in listaFacturas:
                var.ui.tbl_facturas.setRowCount(index + 1)
                var.ui.tbl_facturas.setItem(index, 0, QtWidgets.QTableWidgetItem(str(factura[0])))# Columna Nº
                var.ui.tbl_facturas.setItem(index, 1, QtWidgets.QTableWidgetItem(str(factura[1])))# Columna Fecha
                var.ui.tbl_facturas.setItem(index, 2, QtWidgets.QTableWidgetItem(str(factura[2])))# Columna DNI

                container = QWidget()
                hLayout = QHBoxLayout(container)
                hLayout.setContentsMargins(3, 3, 3, 3)  # Remove margins for better alignment

                borrarFactura = QPushButton()
                borrarFactura.setIcon(QIcon('./img/trash-2.svg'))
                borrarFactura.setFixedSize(30,20)
                borrarFactura.clicked.connect(lambda _, row=index: Ventas.eliminarFactura(row))

                hLayout.addWidget(borrarFactura)
                hLayout.setAlignment(borrarFactura, QtCore.Qt.AlignmentFlag.AlignCenter)  # Align the button horizontally

                var.ui.tbl_facturas.setCellWidget(index, 3, container)# Columna borrar

                var.ui.tbl_facturas.item(index, 0).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                var.ui.tbl_facturas.item(index, 1).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                var.ui.tbl_facturas.item(index, 2).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

                index += 1

        except Exception as e:
            print("Error cargando tabla facturas (ventas.py): ",e)

    @staticmethod
    def cargarOneFactura():
        try:
            fila=var.ui.tbl_facturas.selectedItems()
            datos = [dato.text() for dato in fila]

            registro= conexion.Conexion.getFacturaById(datos[0])
            var.ui.txt_NFactura.setText(registro[0])
            var.ui.txt_FechaFactura.setText(registro[1])
            var.ui.txt_DNIFactura.setText(registro[2])
            var.ui.txt_NombreCliFactura.setText(registro[3])
            var.ui.txt_ApellidosCliFactura.setText(registro[4])

            #Deshabilitar boton crear
            var.ui.btn_GuardarFactura.setEnabled(False)
            #Cargar tabla ventas
            Ventas.cargarTablaVentas()


        except Exception as e:
            print("Error cargando one factura (ventas.py): ",e)

    @staticmethod
    def eliminarFactura(row):
        try:
            nFactura = var.ui.tbl_facturas.item(row, 0).text()

            if len(conexion.Conexion.getVentasFromFactura(nFactura)) >0:
                eventos.Eventos.alertMaker("Critical", "Aviso", "No se pueden borrar facturas que contengan ventas")
                return
            if conexion.Conexion.eliminarFactura(nFactura):
                eventos.Eventos.alertMaker("Information", "Aviso", "Factura borrada")
                Ventas.cargarTablaFacturas()

        except Exception as e:
            print("Error eliminando factura (ventas.py): ",e)

    @staticmethod
    def guardarVenta():
        try:
            nuevaVenta = [var.ui.txt_NFactura.text().strip(), var.ui.txt_codpropventas.text().strip(), var.ui.txt_idVendedorVenta.text().strip() if var.ui.txt_idVendedorVenta else None]
            if conexion.Conexion.altaVenta(nuevaVenta):
                #Deja la propiedada como no disponible
                conexion.Conexion.setEstadoVendido(var.ui.txt_codpropventas.text().strip(), var.ui.txt_FechaFactura.text().strip().strip())
                #Recargar tabla propiedades
                propiedades.Propiedades.cargaTablaPropiedades(None,1)
                eventos.Eventos.alertMaker("Information", "Information", "Venta guardada en la base de datos")
                Ventas.cargarTablaVentas()
            else:
                QtWidgets.QMessageBox.critical('Error', 'Error', 'No se pudo guardar la venta en la base de datos.',
                                               QtWidgets.QMessageBox.StandardButton.Cancel)

        except Exception as e:
            print("Error guardando venta (ventas.py): ", e)

    @staticmethod
    def cargarTablaVentas():
        try:
            listaVentas = conexion.Conexion.getVentasFromFactura(var.ui.txt_NFactura.text().strip())
            if len(listaVentas) == 0:
                var.ui.tbl_ventas.clearContents()
                var.ui.tbl_ventas.setRowCount(1)
                var.ui.tbl_ventas.setItem(0, 0, QtWidgets.QTableWidgetItem("No se encontraron ventas"))
                var.ui.tbl_ventas.setSpan(0, 0, 1, var.ui.tbl_ventas.columnCount())  # Span all columns
                var.ui.tbl_ventas.item(0, 0).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                return
            else:
                var.ui.tbl_ventas.setSpan(0, 0, 1, 1)  # Span all columns

            var.ui.tbl_ventas.clearContents()
            index = 0
            for venta in listaVentas:
                propiedad=conexion.Conexion.getPropiedadById(venta[2])
                var.ui.tbl_ventas.setRowCount(index + 1)
                var.ui.tbl_ventas.setItem(index, 0, QtWidgets.QTableWidgetItem(str(venta[0])))  # ID VENTA
                var.ui.tbl_ventas.setItem(index, 1, QtWidgets.QTableWidgetItem(str(venta[2])))  # ID Propiedad
                var.ui.tbl_ventas.setItem(index, 2, QtWidgets.QTableWidgetItem(str(propiedad[1])))  # Dirección
                var.ui.tbl_ventas.setItem(index, 3, QtWidgets.QTableWidgetItem(str(propiedad[2])))  # Municipio
                var.ui.tbl_ventas.setItem(index, 4, QtWidgets.QTableWidgetItem(str(propiedad[3])))  # Tipo
                var.ui.tbl_ventas.setItem(index, 5, QtWidgets.QTableWidgetItem(str(propiedad[4])+" €  "))  # Precio

                container = QWidget()
                hLayout = QHBoxLayout(container)
                hLayout.setContentsMargins(3, 3, 3, 3)  # Remove margins for better alignment

                borrarVenta = QPushButton()
                borrarVenta.setIcon(QIcon('./img/trash-2.svg'))
                borrarVenta.setFixedSize(30, 20)
                borrarVenta.clicked.connect(lambda _, row=index: Ventas.eliminarVenta(row))

                hLayout.addWidget(borrarVenta)
                hLayout.setAlignment(borrarVenta,
                                     QtCore.Qt.AlignmentFlag.AlignCenter)  # Align the button horizontally

                var.ui.tbl_ventas.setCellWidget(index, 6, container)  # Columna borrar

                var.ui.tbl_ventas.item(index, 0).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                var.ui.tbl_ventas.item(index, 1).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                var.ui.tbl_ventas.item(index, 2).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                var.ui.tbl_ventas.item(index, 3).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                var.ui.tbl_ventas.item(index, 4).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                var.ui.tbl_ventas.item(index, 5).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter)

                index += 1

            Ventas.calcularTotales()

        except Exception as e:
            print("Error cargando tabla facturas (ventas.py): ", e)

    @staticmethod
    def calcularTotales():
        try:
            subtotal = 0.0
            impuestos = 0.0
            total = 0.0

            # Get the table widget
            table = var.ui.tbl_ventas

            # Iterate through the rows and sum up the values in the specified column
            for row in range(var.ui.tbl_ventas.rowCount()):
                item = var.ui.tbl_ventas.item(row, 5)
                if item.text().strip():
                    try:
                        subtotal += float(item.text()[:-4])  # Convert text to float and add to total
                    except ValueError:
                        print(f"Warning: Non-numeric value found in row {row}, column 5")

            impuestos = subtotal*0.10
            total= subtotal+impuestos

            var.ui.txt_subtotal.setText(str(subtotal))
            var.ui.txt_impuestos.setText(str(impuestos))
            var.ui.txt_total.setText(str(total))


        except Exception as e:
            print("Error calculating totals:", e)
            return None

    @staticmethod
    def eliminarVenta(row):
        print("Elimina", row)
        try:
            nVenta = var.ui.tbl_ventas.item(row, 0).text()
            print("nVenta: ", nVenta)
            nPiso = var.ui.tbl_ventas.item(row, 1).text()

            if conexion.Conexion.eliminarVenta(nVenta):
                #Poner el piso como disponible
                conexion.Conexion.setEstadoDisponible(nPiso)
                Ventas.cargarTablaVentas()
                propiedades.Propiedades.cargaTablaPropiedades(None,1)
                eventos.Eventos.alertMaker("Information", "Aviso", "Venta borrada, la propiedad vuelve a estar disponible")


        except Exception as e:
            print("Error eliminando venta (ventas.py): ", e)