from datetime import  datetime
from dlgCalendar import*

import var
import eventos

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