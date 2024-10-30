from datetime import  datetime
from dlgCalendar import*
from dlgTipoProp import*

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


