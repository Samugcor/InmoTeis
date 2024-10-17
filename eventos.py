'''
Eventos que no tienen que ver con la gestion dde la db
'''
import locale
import os.path
import sys
import time
import re
from datetime import datetime

import clientes
import conexion
import zipfile
import shutil

from PyQt6 import QtWidgets
from PyQt6.QtGui import QIcon


import conexionserver
import eventos
import var

#Establecer configuracion regional
locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
locale.setlocale(locale.LC_MONETARY, 'es_ES.UTF-8')

class Eventos:
    #Pop up salir
    def mensajeSalir(self):
        mbox =QtWidgets.QMessageBox()
        mbox.setWindowIcon(QIcon('./img/house.svg'))
        mbox.setIcon(QtWidgets.QMessageBox.Icon.Question)
        mbox.setWindowTitle('Salir')
        mbox.setText('¿Desea usted salir?')
        mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
        mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.No)
        mbox.button(QtWidgets.QMessageBox.StandardButton.Yes).setText('Si')
        mbox.button(QtWidgets.QMessageBox.StandardButton.No).setText('No')

        if mbox.exec() == QtWidgets.QMessageBox.StandardButton.Yes:
            sys.exit()
        else:
            mbox.hide()

    '''
        CARGAR VALORES
    '''
    def cargarProvincias(self):
        var.ui.cmbProvCli.clear()
        listado=conexion.Conexion.listaProv(self)
        #listado = conexionserver.ConexionServer.listaProv(self)
        var.ui.cmbProvCli.addItems(listado)

    def cargarMunicipios(self):
        provincia=var.ui.cmbProvCli.currentText()
        var.ui.cmbMunicipioCli.clear()
        listado=conexion.Conexion.listaMuni(provincia)
        #listado = conexionserver.ConexionServer.listaMuniProv(provincia)
        var.ui.cmbMunicipioCli.addItems(listado)

    def cargaFecha(qDate):
        try:
            data = ('{:02d}/{:02d}/{:4d}'.format(qDate.day(), qDate.month(), qDate.year()))
            if var.panel == var.ui.panPrincipal.currentIndex() and var.btn==0:
                var.ui.txtAltaCliente.setText(str(data))
            elif var.panel == var.ui.panPrincipal.currentIndex() and var.btn==1:
                var.ui.txtBajaCliente.setText(str(data))
            time.sleep(0.2)
            var.uiCalendar.hide()
            return data
        except Exception as error:
            print("error en cargar fecha: ", error)

    '''
        VALIDACIÓN DATOS
    '''
    def validarMail(mail):
        mail = mail.lower()
        regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'
        if re.match(regex, mail) or mail == "":
            return True
        else:
            return False
    def validarDNIcli(dni):
        try:
            dni = str(dni).upper()
            var.ui.txtDniCliente.setText(str(dni))
            tabla = "TRWAGMYFPDXBNJZSQVHLCKE"
            dig_ext = "XYZ"
            reemp_dig_ext = {'X': '0', 'Y': '1', 'Z': '2'}
            numeros = "1234567890"
            if len(dni) == 9:
                dig_control = dni[8]
                dni = dni[:8]
                if dni[0] in dig_ext:
                    dni = dni.replace(dni[0], reemp_dig_ext[dni[0]])

                if len(dni) == len([n for n in dni if n in numeros]) and tabla[int(dni) % 23] == dig_control:
                    var.ui.txtDniCliente.setStyleSheet("background-color:rgb(255, 255, 222);")
                    return True
                else:
                    return False
            else:
                return False

        except Exception as error:
            print("error en validar dni ", error)

    '''
        BACKUP
    '''
    def crearBackup(self):
        try:
            fecha=datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
            copia=str(fecha)+"_backup.zip"

            directorio, fichero = var.dlgabrir.getSaveFileName(None,"Guardar Copia Seguridad",copia,'.zip')
            if var.dlgabrir.accept and fichero:
                fichezip=zipfile.ZipFile(fichero,'w')
                fichezip.write('bbdd.sqlite',os.path.basename('bbdd.sqlite'),zipfile.ZIP_DEFLATED)
                fichezip.close()
                shutil.move(fichero,directorio)

                mbox = QtWidgets.QMessageBox()
                mbox.setWindowIcon(QIcon('./img/house.svg'))
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setWindowTitle('Copia de seguridad')
                mbox.setText('Copia de seguridad creada')
                mbox.setStandardButtons(
                    QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')

                mbox.exec()

        except Exception as error:
            print("error en crear backup: ", error)

    def restauraraBackup(self):
        try:
            filename=var.dlgabrir.getOpenFileName(None,"Restaurar Copia Seguridad",'','*.zip;;All Files (*)')
            file=filename[0]
            if file:
                with zipfile.ZipFile(file,'r') as bbdd:
                    bbdd.extractall(pwd=None)
                bbdd.close()

                mbox = QtWidgets.QMessageBox()
                mbox.setWindowIcon(QIcon('./img/house.svg'))
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setWindowTitle('Copia de seguridad')
                mbox.setText('Copia de seguridad restaurada')
                mbox.setStandardButtons(
                    QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')

                mbox.exec()
                conexion.Conexion.db_conexion(self)
                eventos.Eventos.cargarProvincias(self)
                clientes.Clientes.cargaTablaCientes(self)

        except Exception as e:
            print("error en restaurar backup: ", e)

    '''
        OTROS
    '''
    def abrirCalendar(pan, btn):
        try:
            var.panel = pan
            var.btn = btn
            var.uiCalendar.show()
        except Exception as error:
            print("error en abrir calendar ", error)

    def resizeTablaClientes(self):
        try:
            header=var.ui.tabClientes.horizontalHeader()
            for i in range(header.count()):
                if(i in (1,2,4,5)):
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.Stretch)
                else:
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)

                header_items =var.ui.tabClientes.horizontalHeaderItem(i)
                font= header_items.font()
                font.setBold(True)
                header_items.setFont(font)

        except Exception as e:
            print("error en resize tabla clientes ", e)

    def limpiarPanel(self):
        camposPanel = [var.ui.txtDniCliente, var.ui.txtAltaCliente, var.ui.txtApellidosCliente,
                    var.ui.txtNombreCliente, var.ui.txtEmailCliente, var.ui.txtMovilCliente,
                    var.ui.txtDirecionCliente, var.ui.cmbProvCli, var.ui.cmbMunicipioCli, var.ui.txtBajaCliente]

        for i, dato in enumerate(camposPanel):
            if i==7 or i==8:
                pass
            else:
                dato.setText("")

            eventos.Eventos.cargarProvincias(self)