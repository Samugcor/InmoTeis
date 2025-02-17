from PyQt6.QtWidgets import QPushButton, QHBoxLayout, QWidget
from PyQt6 import QtWidgets, QtCore
from PyQt6.QtGui import QIcon

import conexion
import var


class Alquileres:
    @staticmethod
    def cargarTablaContratos():
        try:
            listaContratos=conexion.Conexion.listaContratos()

            if len(listaContratos) == 0:
                var.ui.tbl_contratos.clearContents()
                var.ui.tbl_contratos.setRowCount(1)
                var.ui.tbl_contratos.setItem(0, 0, QtWidgets.QTableWidgetItem("No se encontraron facturas"))
                var.ui.tbl_contratos.setSpan(0, 0, 1, var.ui.tbl_contratos.columnCount())  # Span all columns
                var.ui.tbl_contratos.item(0, 0).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                return
            else:
                var.ui.tbl_contratos.setSpan(0, 0, 1, 1)  # Span all columns


            var.ui.tbl_contratos.clearContents()
            index=0
            for contrato in listaContratos:
                var.ui.tbl_contratos.setRowCount(index + 1)
                var.ui.tbl_contratos.setItem(index, 0, QtWidgets.QTableWidgetItem(str(contrato[0])))# Columna Nº
                var.ui.tbl_contratos.setItem(index, 1, QtWidgets.QTableWidgetItem(str(contrato[1])))# Columna DNI

                container = QWidget()
                hLayout = QHBoxLayout(container)
                hLayout.setContentsMargins(3, 3, 3, 3)  # Remove margins for better alignment

                borrarContrato = QPushButton()
                borrarContrato.setIcon(QIcon('./img/trash-2.svg'))
                borrarContrato.setFixedSize(30,20)
                borrarContrato.clicked.connect(lambda _, row=index: Alquileres.eliminarContrato(row))

                hLayout.addWidget(borrarContrato)
                hLayout.setAlignment(borrarContrato, QtCore.Qt.AlignmentFlag.AlignCenter)  # Align the button horizontally

                var.ui.tbl_contratos.setCellWidget(index, 2, container)# Columna borrar

                var.ui.tbl_contratos.item(index, 0).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                var.ui.tbl_contratos.item(index, 1).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

                index += 1
        except Exception as e:
            print("Error cargando tabla de contratos: ",e)

    @staticmethod
    def cargarOneContrato():
        try:
            fila = var.ui.tbl_contratos.selectedItems()
            datos = [dato.text() for dato in fila]

            registro = conexion.Conexion.getContratoById(datos[0])

            var.ui.txt_nContrato_alquiler.setText(registro[0])
            var.ui.txt_idVendedor_alquiler.setText(registro[1])
            var.ui.txt_fechaFirma_alquiler.setText(registro[2])
            var.ui.txt_fechaInicio_alquiler.setText(registro[3])
            var.ui.txt_fechaFin_alquiler.setText(registro[4])
            var.ui.txt_idPropiedad_alquiler.setText(registro[5])
            var.ui.txt_direccion_alquiler.setText(registro[6])
            var.ui.txt_municipio_alquiler.setText(registro[7])
            var.ui.txt_cp_alquiler.setText(registro[8])
            var.ui.txt_dni_alquiler.setText(registro[9])
            var.ui.txt_nombre_alquiler.setText(registro[10])
            var.ui.txt_apellidos_alquiler.setText(registro[11])


            # Cargar tabla menusalidades


        except Exception as e:
            print("Error cargando one contrato (ventas.py): ", e)
    @classmethod
    def eliminarContrato(row):
        print("Eliminar ",row)