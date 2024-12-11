from calendar import Calendar
from idlelib.help_about import AboutDialog

import conexionserver
import propiedades
import vendedor
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
        var.npaginacli = 0
        var.npaginapro = 0
        var.uiCalendar = Calendar()
        var.dlgabrir = FileDialogAbrir()
        var.dlggestion = DlgGestionProp()
        var.dlgabout = DlgAbout()
        var.conexionMode = True


        var.ui.rgEstado.setId(var.ui.rbtAlquilado, 1)
        var.ui.rgEstado.setId(var.ui.rbtVendido, 2)
        var.ui.rgEstado.setId(var.ui.rbtDisponible, 3)

        self.setStyleSheet(styles.load_stylesheet())



        '''Conexiones: cambia var.conexionMode para usar una u otra conexion'''
        if var.conexionMode:
            print("Usando db_conexion, la conexion con la base de datos del proyecto")
            conexion.Conexion.db_conexion(self)
        else:
            print("Usando ConexionServer, la conexion con la base de datos del servidor")
            conexionserver.ConexionServer.crear_conexion(self)

        propiedades.Propiedades.formPropiedad(self)
        eventos.Eventos.cargarFiltros(self)
        var.ui.cmbFiltroTipoProp.setEditable(True)

        '''
        Eventos formulario
        '''
        var.ui.txtBajaProp.textChanged.connect(propiedades.Propiedades.formPropiedad)
        var.ui.txtPrecioVentaProp.textChanged.connect(propiedades.Propiedades.formPropiedad)
        var.ui.txtPrecioAlquilerProp.textChanged.connect(propiedades.Propiedades.formPropiedad)

        '''
        Eventos de Tablas
        '''
        clientes.Clientes.cargaTablaCientes(self,1)
        eventos.Eventos.resizeTablaClientes(self)
        var.ui.tabClientes.clicked.connect(clientes.Clientes.cargaOneCliente)


        propiedades.Propiedades.cargaTablaPropiedades(self,1)
        eventos.Eventos.resizeTablaPropiedades(self)
        var.ui.tabPropiedades.clicked.connect(propiedades.Propiedades.cargaOnePropiedad)

        vendedor.Vendedor.cargaTablaVendedores(self)
        eventos.Eventos.resizeTablaVendedores(self)
        var.ui.tabVendedores.clicked.connect(vendedor.Vendedor.cargaOneVendedor)


        '''
        Zona de eventos del menubar
        '''
        var.ui.actionSalir.triggered.connect(eventos.Eventos.mensajeSalir)
        var.ui.actionCrear_Backup.triggered.connect(eventos.Eventos.crearBackup)
        var.ui.actionRestaurar_Backup.triggered.connect(eventos.Eventos.restauraraBackup)
        var.ui.actionTipo_propiedades.triggered.connect(eventos.Eventos.abrirTipoProp)
        var.ui.actionExportar_propiedades_JSON.triggered.connect(eventos.Eventos.exportJSONProp)
        var.ui.actionExportar_vendedores_JSON.triggered.connect(eventos.Eventos.exportJSONVendedores)
        var.ui.actionExportar_propiedades_CSV.triggered.connect(eventos.Eventos.exportCSVProp)
        var.ui.actionAbout.triggered.connect(eventos.Eventos.abrirAbout)
        '''
        Eventos de botones
        '''
        #BOTONES CLIENTES
        var.ui.btnGrabarCli.clicked.connect(clientes.Clientes.altaClientes)
        var.ui.btnAltaCli.clicked.connect(lambda: eventos.Eventos.abrirCalendar(0,0))
        var.ui.btnBajaCli.clicked.connect(lambda: eventos.Eventos.abrirCalendar(0,1))
        var.ui.btnModificarCliente.clicked.connect(clientes.Clientes.modifCliente)
        var.ui.btnEliminarCliente.clicked.connect(clientes.Clientes.bajaCliente)
        var.ui.btnBuscaCliente.clicked.connect(clientes.Clientes.buscarCliente)
        var.ui.btnSiguientePagCli.clicked.connect(eventos.Eventos.pasarPag)
        var.ui.btnAnteriorPagCli.clicked.connect(eventos.Eventos.pasarPag)

        #BOTONES PROPIEDADES
        var.ui.btnAltaProp.clicked.connect(lambda: eventos.Eventos.abrirCalendar(1, 0))
        var.ui.btnBajaProp.clicked.connect(lambda: eventos.Eventos.abrirCalendar(1, 1))
        var.ui.btnGrabarProp.clicked.connect(propiedades.Propiedades.altaPropiedad)
        var.ui.btnModificarProp.clicked.connect(propiedades.Propiedades.modifPropiedad)
        var.ui.btnEliminarProp.clicked.connect(propiedades.Propiedades.bajaPropiedad)
        var.ui.btnSiguientePagProp.clicked.connect(eventos.Eventos.pasarPag)
        var.ui.btnAnteriorPagProp.clicked.connect(eventos.Eventos.pasarPag)

        #BOTONES VENDEDORES
        var.ui.btnGrabarVendedor.clicked.connect(vendedor.Vendedor.altaVendedores)
        var.ui.btnModificarVendedor.clicked.connect(vendedor.Vendedor.modifVendedor)
        var.ui.btnEliminarVendedor.clicked.connect(vendedor.Vendedor.bajaVendedor)
        var.ui.btnAltaVendedor.clicked.connect(lambda: eventos.Eventos.abrirCalendar(3,0))
        var.ui.btnBuscarVendedor.clicked.connect(vendedor.Vendedor.buscarVendedor)



        '''
        Eventos de cajas de texto
        '''
        #CLIENTES
        var.ui.txtDniCliente.editingFinished.connect(lambda: clientes.Clientes.checkDNI(var.ui.txtDniCliente.text()))
        var.ui.txtEmailCliente.editingFinished.connect(clientes.Clientes.checkEmail)
        var.ui.txtMovilCliente.editingFinished.connect(clientes.Clientes.checkMovil)

        #VENDEDORES
        var.ui.txtDniVendedor.editingFinished.connect(lambda: vendedor.Vendedor.checkDNI(var.ui.txtDniCliente.text()))
        var.ui.txtEmailVendedor.editingFinished.connect(vendedor.Vendedor.checkEmail)
        var.ui.txtMovilVendedor.editingFinished.connect(vendedor.Vendedor.checkMovil)

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
        var.ui.chkHistoricoCli.stateChanged.connect(lambda: clientes.Clientes.cargaTablaCientes(self,1))
        var.ui.chkHistoricoProp.stateChanged.connect(lambda: propiedades.Propiedades.cargaTablaPropiedades(self,1))
        var.ui.chkHistoricoVendedores.stateChanged.connect(vendedor.Vendedor.cargaTablaVendedores)
        ''''
        Eventos filtros
        '''

        var.ui.btnBuscarProp.clicked.connect(lambda: propiedades.Propiedades.cargaTablaPropiedades(self,1))
        var.ui.cmbFiltroTipoProp.lineEdit().editingFinished.connect(eventos.Eventos.validarFiltroTipo)
        var.ui.cmbFiltroMuniProp.lineEdit().editingFinished.connect(eventos.Eventos.validarFiltroTipo)

if __name__ == '__main__':

    app = QtWidgets.QApplication([])
    window = Main()
    window.showMaximized()
    sys.exit(app.exec())