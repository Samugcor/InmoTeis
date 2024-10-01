import clientes
import conexion
import eventos
import styles
from venPrincipal import *
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
        self.setStyleSheet(styles.load_stylesheet())
        conexion.Conexion.db_conexion(self)
        eventos.Eventos.cargarProvincias(self)
        eventos.Eventos.cargarMunicipios(self)

        '''
        Zona de eventos del menubar
        '''
        var.ui.actionSalir.triggered.connect(eventos.Eventos.mensajeSalir)

        '''
        Eventos de botones
        '''
        var.ui.btnGrabarCli.clicked.connect(clientes.Clientes.altaClientes)

        '''
        Eventos de cajas de texto
        '''
        var.ui.txtDniCliente.editingFinished.connect(lambda: clientes.Clientes.checkDNI(var.ui.txtDniCliente.text()))


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = Main()
    window.showMaximized()
    sys.exit(app.exec())