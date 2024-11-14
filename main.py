from calendar import Calendar

import conexionserver
import propiedades
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
        var.dlgabrir = FileDialogAbrir()
        var.dlggestion = DlgGestionProp()

        var.ui.rgEstado.setId(var.ui.rbtAlquilado, 1)
        var.ui.rgEstado.setId(var.ui.rbtVendido, 2)
        var.ui.rgEstado.setId(var.ui.rbtDisponible, 3)

        self.setStyleSheet(styles.load_stylesheet())
        conexion.Conexion.db_conexion(self)
        propiedades.Propiedades.formPropiedad(self)
        eventos.Eventos.cargarFiltros(self)
        var.ui.cmbFiltroTipoProp.setEditable(True)
        #conexionserver.ConexionServer.crear_conexion(self)



        '''
        Eventos formulario
        '''
        var.ui.txtBajaProp.textChanged.connect(propiedades.Propiedades.formPropiedad)
        var.ui.txtPrecioVentaProp.textChanged.connect(propiedades.Propiedades.formPropiedad)
        var.ui.txtPrecioAlquilerProp.textChanged.connect(propiedades.Propiedades.formPropiedad)

        '''
        Eventos de Tablas
        '''
        clientes.Clientes.cargaTablaCientes(self)
        eventos.Eventos.resizeTablaClientes(self)
        var.ui.tabClientes.clicked.connect(clientes.Clientes.cargaOneCliente)
        eventos.Eventos.resizeTablaPropiedades(self)

        propiedades.Propiedades.cargaTablaPropiedades(self)
        var.ui.tabPropiedades.clicked.connect(propiedades.Propiedades.cargaOnePropiedad)

        '''
        Zona de eventos del menubar
        '''
        var.ui.actionSalir.triggered.connect(eventos.Eventos.mensajeSalir)
        var.ui.actionCrear_Backup.triggered.connect(eventos.Eventos.crearBackup)
        var.ui.actionRestaurar_Backup.triggered.connect(eventos.Eventos.restauraraBackup)
        var.ui.actionTipo_propiedades.triggered.connect(eventos.Eventos.abrirTipoProp)
        '''
        Eventos de botones
        '''
        #BOTONES CLIENTES
        var.ui.btnGrabarCli.clicked.connect(clientes.Clientes.altaClientes)
        var.ui.btnAltaCli.clicked.connect(lambda: eventos.Eventos.abrirCalendar(0,0))
        var.ui.btnBajaCli.clicked.connect(lambda: eventos.Eventos.abrirCalendar(0,1))
        var.ui.btnModificarCliente.clicked.connect(clientes.Clientes.modifCliente)
        var.ui.btnEliminarCliente.clicked.connect(clientes.Clientes.bajaCliente)

        #BOTONES PROPIEDADES
        var.ui.btnAltaProp.clicked.connect(lambda: eventos.Eventos.abrirCalendar(1, 0))
        var.ui.btnBajaProp.clicked.connect(lambda: eventos.Eventos.abrirCalendar(1, 1))
        var.ui.btnGrabarProp.clicked.connect(propiedades.Propiedades.altaPropiedad)
        var.ui.btnModificarProp.clicked.connect(propiedades.Propiedades.modifPropiedad)
        var.ui.btnEliminarProp.clicked.connect(propiedades.Propiedades.bajaPropiedad)

        '''
        Eventos de cajas de texto
        '''
        var.ui.txtDniCliente.editingFinished.connect(lambda: clientes.Clientes.checkDNI(var.ui.txtDniCliente.text()))
        var.ui.txtEmailCliente.editingFinished.connect(clientes.Clientes.checkEmail)
        var.ui.txtMovilCliente.editingFinished.connect(clientes.Clientes.checkMovil)

        '''
        Eventos de los combobox
        '''
        eventos.Eventos.cargarProvincias(self,0)
        eventos.Eventos.cargarMunicipios(self)
        eventos.Eventos.cargarTipoPropiedad(self)
        var.ui.cmbProvCli.currentIndexChanged.connect(eventos.Eventos.cargarMunicipios)
        var.ui.cmbProvProp.currentIndexChanged.connect(eventos.Eventos.cargarMunicipios)
        '''
        Eventos ToolBar
        '''
        var.ui.actionSalir.triggered.connect(eventos.Eventos.mensajeSalir)
        var.ui.actionbarLimpiar.triggered.connect(eventos.Eventos.limpiarPanel)

        '''
        Eventos checkbox
        '''
        var.ui.chkHistoricoCli.stateChanged.connect(clientes.Clientes.cargaTablaCientes)
        var.ui.chkHistoricoProp.stateChanged.connect(propiedades.Propiedades.cargaTablaPropiedades)

        ''''
        Eventos filtros
        '''
        if var.ui.btnBuscarProp.isChecked():
            propiedades.Propiedades.cargaTablaPropiedades(self)
            var.ui.cmbFiltroTipoProp.currentIndexChanged.connect(propiedades.Propiedades.cargaTablaPropiedades)
            var.ui.cmbFiltroMuniProp.currentIndexChanged.connect(propiedades.Propiedades.cargaTablaPropiedades)

        var.ui.cmbFiltroTipoProp.lineEdit().editingFinished.connect(eventos.Eventos.validarFiltroTipo)
        var.ui.cmbFiltroMuniProp.lineEdit().editingFinished.connect(eventos.Eventos.validarFiltroTipo)

if __name__ == '__main__':

    app = QtWidgets.QApplication([])
    window = Main()
    window.showMaximized()
    sys.exit(app.exec())