'''
Eventos que no tienen que ver con la gestion dde la db
'''
import csv
import json
import locale
import os.path
import sys
import time
import re
from datetime import datetime
from xmlrpc.client import DateTime

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QCompleter, QApplication

import clientes
import conexion
import zipfile
import shutil

from PyQt6 import QtWidgets
from PyQt6.QtGui import QIcon


import conexionserver
import eventos
import propiedades
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
    def cargarProvincias(self,modo):
        if var.conexionMode:
            listado = conexion.Conexion.listaProv(self)
        else:
            listado = conexionserver.ConexionServer.listaProv(self)

        if modo == 0:
            var.ui.cmbProvCli.clear()
            var.ui.cmbProvCli.addItems(listado)

            var.ui.cmbProvProp.clear()
            var.ui.cmbProvProp.addItems(listado)
        elif modo == 1:
            var.ui.cmbProvCli.clear()
            var.ui.cmbProvCli.addItems(listado)
        elif modo == 2:
            var.ui.cmbProvProp.clear()
            var.ui.cmbProvProp.addItems(listado)
        else:
            print("Error carga provincias modo no valido")

    def cargarFiltros(self):
        #Recoge las listas de cada combo box
        if var.conexionMode:
            listTipoProp = conexion.Conexion.listaTipoPropiedad()
            listMuni = conexion.Conexion.listAllMuni()
        else:
            listTipoProp = conexionserver.ConexionServer.listaTipoPropiedad()
            listMuni = conexionserver.ConexionServer.listAllMuni()

        #Limpia para volver a poner valores, añade el valor -- para cuando no hay nada seleccionado, añade al cmb
        var.ui.cmbFiltroTipoProp.clear()
        listTipoProp.insert(0,"---")
        var.ui.cmbFiltroTipoProp.addItems(listTipoProp)

        completer = QCompleter(listTipoProp, var.ui.cmbFiltroTipoProp)
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        completer.setFilterMode(Qt.MatchFlag.MatchContains)
        var.ui.cmbFiltroTipoProp.setCompleter(completer)


        # Limpia para volver a poner valores, añade el valor -- para cuando no hay nada seleccionado, añade al cmb
        var.ui.cmbFiltroMuniProp.clear()
        listMuni.insert(0,"---")
        var.ui.cmbFiltroMuniProp.addItems(listMuni)

        completer = QCompleter(listMuni, var.ui.cmbFiltroMuniProp)
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        completer.setFilterMode(Qt.MatchFlag.MatchContains)
        var.ui.cmbFiltroMuniProp.setCompleter(completer)

    def cargarMunicipios(self):
        provinciaCli=var.ui.cmbProvCli.currentText()
        provinciaPro=var.ui.cmbProvProp.currentText()

        var.ui.cmbMunicipioCli.clear()
        var.ui.cmbMunicipioProp.clear()

        if var.conexionMode:
            listadoCli=conexion.Conexion.listaMuni(provinciaCli)
            listadoPro=conexion.Conexion.listaMuni(provinciaPro)
        else:
            listadoCli=conexionserver.ConexionServer.listaMuniProv(provinciaCli)
            listadoPro=conexionserver.ConexionServer.listaMuniProv(provinciaPro)


        var.ui.cmbMunicipioCli.addItems(listadoCli)
        var.ui.cmbMunicipioProp.addItems(listadoPro)

    def cargaFecha(qDate):
        try:
            data = ('{:02d}/{:02d}/{:4d}'.format(qDate.day(), qDate.month(), qDate.year()))

            if var.panel == 0 and var.btn==0:
                var.ui.txtAltaCliente.setText(str(data))
            elif var.panel == 0 and var.btn==1:
                var.ui.txtBajaCliente.setText(str(data))
            elif var.panel == 1 and var.btn==0:
                var.ui.txtAltaProp.setText(str(data))
            elif var.panel == 1 and var.btn==1:
                var.ui.txtBajaProp.setText(str(data))
            time.sleep(0.2)
            var.uiCalendar.hide()
            return data
        except Exception as error:
            print("error en cargar fecha: ", error)

    def cargarTipoPropiedad(self):
        var.ui.cmbTipoProp.clear()

        if var.conexionMode:
            listado=conexion.Conexion.listaTipoPropiedad()
        else:
            listado=conexionserver.ConexionServer.listaTipoPropiedad()

        var.ui.cmbTipoProp.addItems(listado)

    '''
        VALIDACIÓN DATOS
    '''
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

    def validarMail(mail):
        mail = mail.lower()
        regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'
        if re.match(regex, mail) or mail == "":
            return True
        else:
            return False

    def validarMovil(movil):
        movil = movil.lower()
        regex = r'^[67]\d{8}$'
        if re.match(regex, movil):
            return True
        else:
            return False

    @staticmethod
    def validarFiltroTipo():
        if var.conexionMode:
            if var.ui.cmbFiltroTipoProp.currentText() not in conexion.Conexion.listaTipoPropiedad():
                var.ui.cmbFiltroTipoProp.lineEdit().setText("---")

            if var.ui.cmbFiltroMuniProp.currentText() not in conexion.Conexion.listAllMuni():
                var.ui.cmbFiltroMuniProp.lineEdit().setText("---")
        else:
            if var.ui.cmbFiltroTipoProp.currentText() not in conexionserver.ConexionServer.listaTipoPropiedad():
                var.ui.cmbFiltroTipoProp.lineEdit().setText("---")

            if var.ui.cmbFiltroMuniProp.currentText() not in conexionserver.ConexionServer.listAllMuni():
                var.ui.cmbFiltroMuniProp.lineEdit().setText("---")

    @staticmethod
    def validarFechaAlta():
        try:
            fechaAlta = datetime.strptime(var.ui.txtAltaCliente.text(), '%d/%m/%Y')


            if var.ui.txtBajaCliente.text():
                try:
                    fechaBaja = datetime.strptime(var.ui.txtBajaCliente.text(), '%d/%m/%Y')
                    if fechaAlta <= fechaBaja:
                        return True
                    else:
                        eventos.Eventos.alertMaker("Critical", "Aviso",
                                                   "La fecha de alta no puede ser posterior a la de baja")
                        return False
                except Exception as error:
                    print("error en convirtiendo fecha baja", error)
            else:
                return True
        except Exception as error:
            print("error en convirtiendo fecha alta", error)

    @staticmethod
    def validarFechaBaja():
        try:
            fechaAlta = datetime.strptime(var.ui.txtAltaCliente.text(), '%d/%m/%Y')
            print(type(fechaAlta))
            print(fechaAlta)
        except Exception as error:
            print("error en convirtiendo fecha alta", error)

        if var.ui.txtBajaCliente.text():
            try:
                fechaBaja = datetime.strptime(var.ui.txtBajaCliente.text(), '%d/%m/%Y')
                print(type(fechaBaja))
                print(fechaBaja)
            except Exception as error:
                print("error en convirtiendo fecha baja", error)
                eventos.Eventos.alertMaker("Critical", "Aviso",
                                           "El formato de la fecha de baja no es valido")
                return False

            if fechaAlta < fechaBaja:
                return True
            else:
                eventos.Eventos.alertMaker("Critical", "Aviso",
                                           "La fecha de baja no puede ser anterior a la fecha de alta")
                return False
        else:
            eventos.Eventos.alertMaker("Critical", "Aviso",
                                       "Para dar de baja a un cliente debe introducir una fecha de baja")
            return False

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
                if var.conexionMode:
                    conexion.Conexion.db_conexion(self)
                else:
                    conexionserver.ConexionServer.crear_conexion(self)

                eventos.Eventos.cargarProvincias(self,1)
                clientes.Clientes.cargaTablaCientes(self,1)

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

    def resizeTablaPropiedades(self):
        try:
            header=var.ui.tabPropiedades.horizontalHeader()
            for i in range(header.count()):
                if(i in (1,2,7)):
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.Stretch)
                else:
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)

                header_items =var.ui.tabPropiedades.horizontalHeaderItem(i)
                font= header_items.font()
                font.setBold(True)
                header_items.setFont(font)

        except Exception as e:
            print("error en resize tabla propiedades ", e)

    def limpiarPanel(self):
        try:
            if var.ui.panPrincipal.currentIndex()==0:
                camposPanel = [var.ui.txtDniCliente, var.ui.txtAltaCliente, var.ui.txtApellidosCliente,
                               var.ui.txtNombreCliente, var.ui.txtEmailCliente, var.ui.txtMovilCliente,
                               var.ui.txtDirecionCliente, var.ui.cmbProvCli, var.ui.cmbMunicipioCli,
                               var.ui.txtBajaCliente]

                for i, dato in enumerate(camposPanel):
                    if i == 7 or i == 8:
                        pass
                    else:
                        dato.setText("")

                eventos.Eventos.cargarProvincias(self,1)
                var.ui.tabClientes.clearSelection()
            else:
                camposProp = [var.ui.lblCodigoPropText, var.ui.txtAltaProp, var.ui.txtBajaProp, var.ui.txtDirecionProp,
                              var.ui.txtCpProp, var.ui.spinHabitaciones, var.ui.spinBanios,
                              var.ui.txtSuperficie, var.ui.txtPrecioAlquilerProp, var.ui.txtPrecioVentaProp,
                              var.ui.areatxtObservacionesProp, var.ui.txtPropietarioProp, var.ui.txtMovilProp]

                for i, dato in enumerate(camposProp):
                    if isinstance(dato, QtWidgets.QSpinBox):
                        dato.setValue(0)
                    else:
                        dato.setText("")

                propiedades.Propiedades.formPropiedad(self)
                var.ui.chkIntercambio.setChecked(False)

                eventos.Eventos.cargarProvincias(self,2)
                eventos.Eventos.cargarTipoPropiedad(self)

                #Borrar filttros
                var.ui.cmbFiltroTipoProp.setCurrentIndex(0)
                var.ui.cmbFiltroMuniProp.setCurrentIndex(0)

                propiedades.Propiedades.cargaTablaPropiedades(self,1)

        except Exception as e:
            print("error al limpiar panel (eventos.py): ", e)

    def abrirTipoProp(self):
        try:
            var.dlggestion.show()
        except Exception as e:
            print("Error en abrir  ventana tipo prop ", e)

    def abrirAbout(self):
        try:
            var.dlgabout.show()
        except Exception as e:
            print("Error en abrir  ventana tipo prop ", e)

    @staticmethod
    def alertMaker(tipo,titulo,mensaje):

        mbox = QtWidgets.QMessageBox()
        mbox.setWindowIcon(QIcon('./img/house.svg'))
        if tipo == "Information":
            mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
        elif tipo == "Critical":
            mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)

        mbox.setWindowTitle(titulo)
        mbox.setText(mensaje)
        mbox.setStandardButtons(
            QtWidgets.QMessageBox.StandardButton.Ok)
        mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
        mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')

        mbox.exec()


    def pasarPag(self):
        if QApplication.instance().sender().objectName() == "btnSiguientePagCli":
            print("btnsiguiente cli")
            var.npaginacli = var.npaginacli + 1
            clientes.Clientes.cargaTablaCientes(self,0)

        elif QApplication.instance().sender().objectName() == "btnAnteriorPagCli":
            print("btnanterior cli")
            var.npaginacli = var.npaginacli - 1
            clientes.Clientes.cargaTablaCientes(self,0)

        elif QApplication.instance().sender().objectName() == "btnSiguientePagProp":
            print("btnsiguiente prop")

            var.npaginapro = var.npaginapro + 1
            propiedades.Propiedades.cargaTablaPropiedades(self,0)

        elif QApplication.instance().sender().objectName() == "btnAnteriorPagProp":
            print("btnanterior pro")

            var.npaginapro = var.npaginapro - 1
            propiedades.Propiedades.cargaTablaPropiedades(self,0)

        else:
            print("Error en pasar pagina")



    '''
    EXPORTAR
    '''

    def exportCSVProp(self):
        try:
            fecha = datetime.today()
            fecha = fecha.strftime('%Y_%m_%d_%H_%M_%S')
            file = (str(fecha) + '_DatosPropiedades.csv')
            directorio, fichero = var.dlgabrir.getSaveFileName(None, "Exporta Datos en CSV", file, ".csv")
            if fichero:
                if var.conexionMode:
                    registros = conexion.Conexion.listadoAllPropiedades(self)
                #else:
                    #⭕registros = conexionserver.ConexionServer

                with open(fichero, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(
                        ["Codigo", "Alta", "Baja", "Dirección", "Provincia", "Municipio","Código Postal", "Tipo", "NºHabitaciones",
                         "NºBaños", "Superficie", "Precio Alquiler", "Precio Venta",
                          "Observaciones", "Operación", "Estado", "Propietario", "Móvil"])
                    for registro in registros:
                        writer.writerow(registro)
                shutil.move(fichero, directorio)
            else:
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                mbox.setWindowTitle("Error")
                mbox.setText("Error Exportación de Datos propiedades.")
                mbox.setStandardButtons(
                    QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
                mbox.exec()

        except Exception as e:
            print("Error al intentar exportar a CSV en Eventos exportCSVProp ", e)

    def exportJSONProp(self):
        try:
            # Generate timestamped filename
            fecha = datetime.today()
            fecha = fecha.strftime('%Y_%m_%d_%H_%M_%S')
            file = (str(fecha) + '_DatosPropiedades.json')

            # Open a save file dialog
            directorio, fichero = var.dlgabrir.getSaveFileName(None, "Exporta Datos en JSON", file, ".json")
            if fichero:
                # Fetch all property records
                if var.conexionMode:
                    registros = conexion.Conexion.listadoAllPropiedades(self)
                #else:
                    #⭕registros = conexionserver.ConexionServer

                # Prepare data for JSON (list of dictionaries)
                keys = ["Codigo", "Alta", "Baja", "Direccion", "Provincia", "Municipio","Codigo_Postal", "Tipo", "N_Habitaciones",
                         "N_Baños", "Superficie", "Precio_Alquiler", "Precio_Venta",
                          "Observaciones", "Operacion", "Estado", "Propietario", "Movil"]
                json_data = [dict(zip(keys, registro)) for registro in registros]

                # Write to JSON file
                with open(fichero, 'w', encoding='utf-8') as jsonfile:
                    json.dump(json_data, jsonfile, ensure_ascii=False, indent=4)

                # Move file to chosen directory
                shutil.move(fichero, directorio)
            else:
                # Handle case where no file was selected
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                mbox.setWindowTitle("Error")
                mbox.setText("Error Exportación de Datos propiedades.")
                mbox.setStandardButtons(
                    QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
                mbox.exec()

        except Exception as e:
            print("Error al intentar exportar a JSON en Eventos exportJSONProp ", e)
