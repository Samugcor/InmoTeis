from tabnanny import check

from PyQt6 import QtWidgets

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
        dni=var.ui.txtDniCliente.text()

        print(dni)