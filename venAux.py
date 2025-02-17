from datetime import  datetime

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QCompleter

import conexion
import informes
from dlgAbout import Ui_Dialog
from dlgCalendar import*
from dlgCrearContrato import*
from dlgInformePropiedades import*
from dlgTipoProp import*
from dlgVendedores import *

import var
import eventos
import propiedades

class Calendar(QtWidgets.QDialog):
    def __init__(self):
        super(Calendar, self).__init__()

        var.uiCalendar=Ui_dlgCalendar()
        var.uiCalendar.setupUi(self)
        dia=datetime.now().day
        mes=datetime.now().month
        ano=datetime.now().year

        var.uiCalendar.Calendar.setSelectedDate((QtCore.QDate(ano,mes,dia)))
        var.uiCalendar.Calendar.clicked.connect(eventos.Eventos.cargaFecha)

class FileDialogAbrir(QtWidgets.QFileDialog):
    def __init__(self):
        super(FileDialogAbrir, self).__init__()

class DlgGestionProp(QtWidgets.QDialog):
    def __init__(self):
        super(DlgGestionProp, self).__init__()
        self.ui = Ui_GestiontipoProp()
        self.ui.setupUi(self)

        self.ui.btnAltaTipoProp.clicked.connect(propiedades.Propiedades.altaTipoPropiedades)
        self.ui.btnEliminarTipoProp.clicked.connect(propiedades.Propiedades.bajaTipoPropiedades)

class DlgAbout (QtWidgets.QDialog):
    def __init__(self):
        super(DlgAbout, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.ui.btnCerrarAbout.clicked.connect(self.close)

class DlgInformeProp(QtWidgets.QDialog):
    def __init__(self):
        super(DlgInformeProp, self).__init__()
        self.ui = Ui_InformeProp()
        self.ui.setupUi(self)

        self.ui.btn_informeCancelar.clicked.connect(self.close)

        self.ui.btn_informeAceptar.clicked.connect(self.aceptarYCerrarVentana)

    def aceptarYCerrarVentana(self):
        try:
            muniSeleccionado = self.ui.cmb_informeMunicipio.currentText()
            print(muniSeleccionado)
            listaPropiedades = conexion.Conexion.listaPropiedadesByMuni(muniSeleccionado)
        except Exception as e:
            print("Error recuperando datos para generar el informe: ",e)

        informes.Informes.reportPropiedades(muniSeleccionado,listaPropiedades)
        self.close()

class DlgSeleccionarVendedor(QtWidgets.QDialog):
    def __init__(self):
        super(DlgSeleccionarVendedor, self).__init__()
        self.ui = Ui_dlgSeleccionVendedores()
        self.ui.setupUi(self)

        self.ui.btn_cancelar.clicked.connect(self.close)

        self.ui.btn_aceptar.clicked.connect(self.aceptarYCerrarVentana)




    def aceptarYCerrarVentana(self):
        try:
            index = self.ui.cmb_vendedores.currentIndex()
            data = self.ui.cmb_vendedores.itemData(index)
            print(data)
            if data:
                var.ui.txt_idVendedorVenta.setText(str(data['id']))
                var.ui.txt_nombreVendedoreVenta.setText(str(data['nombre']))
        except Exception as e:
            print("Error recuperando datos para seleccionar al vendedor: ", e)


        self.close()

class DlgCrearContrato (QtWidgets.QDialog):
    def __init__(self):
        super(DlgCrearContrato, self).__init__()
        self.ui = Ui_CrearContrato()
        self.ui.setupUi(self)


        self.ui.btn_fechafirma.clicked.connect(var.uiCalendar.show)
