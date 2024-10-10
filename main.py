from calendar import Calendar
from venPrincipal import *
from venAux import *

import clientes
import conexion
import eventos
import styles

import sys
import var

class Main(QtWidgets.QMainWindow):

    def __init__(self):
        '''
        Configuración inicial
        '''
        super(Main,self).__init__()
        var.ui = Ui_venPrincipal()
        var.ui.setupUi(self)
        var.uiCalendar = Calendar()
        self.setStyleSheet(styles.load_stylesheet())
        conexion.Conexion.db_conexion(self)
        eventos.Eventos.cargarProvincias(self)
        eventos.Eventos.cargarMunicipios(self)
        clientes.Clientes.cargaTablaCientes(self)
        eventos.Eventos.resizeTablaClientes(self)

        '''
        Zona de eventos del menubar
        '''
        var.ui.actionSalir.triggered.connect(eventos.Eventos.mensajeSalir)

        '''
        Eventos de botones
        '''
        var.ui.btnGrabarCli.clicked.connect(clientes.Clientes.altaClientes)
        var.ui.btnAltaCli.clicked.connect(lambda: eventos.Eventos.abrirCalendar(0))

        '''
        Eventos de cajas de texto
        '''
        var.ui.txtDniCliente.editingFinished.connect(lambda: clientes.Clientes.checkDNI(var.ui.txtDniCliente.text()))
        var.ui.txtEmailCliente.editingFinished.connect(lambda: clientes.Clientes.checkEmail(var.ui.txtEmailCliente.text()))

        '''
        Eventos de los combobox
        '''
        var.ui.cmbProvCli.currentIndexChanged.connect(eventos.Eventos.cargarMunicipios)




if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = Main()
    window.showMaximized()
    sys.exit(app.exec())