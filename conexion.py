import os
from idlelib import query

from PyQt6 import QtSql, QtWidgets
from PyQt6.QtGui import QIcon
from PyQt6.uic.properties import QtCore

import var


class Conexion:

    """
    @staticmethod
    método de una clase que no depende de una instancia específica de esa clase.
    Se puede llamarlo directamente a través de la clase, sin necesidad de crear un objeto de esa clase.
    Es útil en comportamientos o funcionalidades que son más a una clase en general que a una instancia en particular.

    """

    @staticmethod
    def db_conexion(self):
        # Verifica si el archivo de base de datos existe
        if not os.path.isfile('bbdd.sqlite'):
            QtWidgets.QMessageBox.critical(None, 'Error', 'El archivo de la base de datos no existe.',
                                           QtWidgets.QMessageBox.StandardButton.Cancel)
            return False
        # Crear la conexión con la base de datos SQLite
        db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('bbdd.sqlite')

        if db.open():
            # Verificar si la base de datos contiene tablas
            query = QtSql.QSqlQuery()
            query.exec("SELECT name FROM sqlite_master WHERE type='table';")

            if not query.next():  # Si no hay tablas
                QtWidgets.QMessageBox.critical(None, 'Error', 'Base de datos vacía o no válida.',
                                               QtWidgets.QMessageBox.StandardButton.Cancel)
                return False
            else:
                QtWidgets.QMessageBox.information(None, 'Aviso', 'Conexión Base de Datos realizada',
                                               QtWidgets.QMessageBox.StandardButton.Ok)
                return True
        else:
            QtWidgets.QMessageBox.critical(None, 'Error', 'No se pudo abrir la base de datos.',
                                           QtWidgets.QMessageBox.StandardButton.Cancel)
            return False

    @staticmethod
    def listaProv(self):
        listaprov=[]
        query= QtSql.QSqlQuery()
        query.prepare("SELECT * FROM provincias")

        if query.exec():
            while query.next():
                listaprov.append(query.value(1))

        return listaprov

    @staticmethod
    def listaMuni(provincia):
        listamunicipios = []
        query = QtSql.QSqlQuery()
        query.prepare("SELECT * FROM municipios where idprov = (select idprov from provincias where provincia = :provincia)")
        query.bindValue(":provincia", provincia)
        if query.exec():
            while query.next():
                listamunicipios.append(query.value(1))
        return listamunicipios

    def altaCliente(nuevoCli):
        try:

            query = QtSql.QSqlQuery()
            query.prepare("INSERT into clientes"
                          " VALUES (:dnicli,:altacli,:apecli,:nomecli,:emailcli,:movilcli,:direcli,:provcli,:municli, :bajacli)")

            '''Con este bucle si un campo se queda vacio si guarda como string vacia en vez de null, habría que arreglarlo
            fields = [
                ":dnicli", ":altacli", ":apecli", ":nomecli", ":emailcli",
                ":movilcli", ":direcli", ":provcli", ":municli"
            ]

            for field, value in zip(fields, nuevoCli):
                query.bindValue(field, str(value))'''

            #if str empty =null
            # null if not str(nuevoCli[0]) else str(nuevoCli[0])
            query.bindValue(":dnicli", None if not str(nuevoCli[0]) else str(nuevoCli[0]))
            query.bindValue(":altacli", None if not str(nuevoCli[1]) else str(nuevoCli[1]))
            query.bindValue(":apecli", None if not str(nuevoCli[2]) else str(nuevoCli[2]))
            query.bindValue(":nomecli", None if not str(nuevoCli[3]) else str(nuevoCli[3]))
            query.bindValue(":emailcli", None if not str(nuevoCli[4]) else str(nuevoCli[4]))
            query.bindValue(":movilcli", None if not str(nuevoCli[5]) else str(nuevoCli[5]))
            query.bindValue(":direcli", None if not str(nuevoCli[6]) else str(nuevoCli[6]))
            query.bindValue(":provcli", None if not str(nuevoCli[7]) else str(nuevoCli[7]))
            query.bindValue(":municli", None if not str(nuevoCli[8]) else str(nuevoCli[8]))
            query.bindValue(":bajacli", None if not str(nuevoCli[9]) else str(nuevoCli[9]))

            if query.exec():
                print("Cliente añadido")
                return True
            else:
                return False
        except Exception as e:
            print("Error alta cliente",e)

    def listadoClientes(self):
        try:
            listado=[]
            if var.ui.chkHistoricoCli.isChecked():
                query = QtSql.QSqlQuery()
                #Where fecha baja = null
                query.prepare("SELECT * FROM clientes ORDER BY apecli, nomecli ASC")

                if query.exec():
                    while query.next():
                        fila = [query.value(i) for i in range(query.record().count())]
                        listado.append(fila)
                return listado
            else:
                query = QtSql.QSqlQuery()
                # Where fecha baja = null
                query.prepare("SELECT * FROM clientes WHERE bajacli IS null ORDER BY apecli, nomecli ASC")

                if query.exec():
                    while query.next():
                        fila = [query.value(i) for i in range(query.record().count())]
                        listado.append(fila)
                return listado
        except Exception as e:
            print("Error recuperando el listado de clientes",e)

    def datosOneCliente(dni):
        try:
            registro = []
            query = QtSql.QSqlQuery()
            query.prepare("SELECT * FROM clientes WHERE dnicli = :dni")

            query.bindValue(":dni",str(dni).strip())

            if query.exec():
                while query.next():
                   for i in range(query.record().count()):
                    registro.append(str(query.value(i)))

            return registro

        except Exception as e:
            print("Error recuperando datos de clientes",e)

    def modifCliente(registro):
        try:
            query=QtSql.QSqlQuery()
            query.prepare("UPDATE clientes SET altacli =:altacli, apecli = :apecli, nomecli = :nomecli, emailcli = :emailcli, "
                          " movilcli = :movilcli, direcli = :direcli, provcli = :provcli, municli = :municli, bajacli = :bajacli "
                          " WHERE dnicli = :dni")

            query.bindValue(":dni", None if not(str(registro[0]))else str(registro[0]))
            query.bindValue(":altacli", None if not (str(registro[1])) else str(registro[1]))
            query.bindValue(":apecli", None if not (str(registro[2])) else str(registro[2]))
            query.bindValue(":nomecli", None if not (str(registro[3])) else str(registro[3]))
            query.bindValue(":emailcli", None if not str(registro[4]) else str(registro[4]))
            query.bindValue(":movilcli", None if not (str(registro[5])) else str(registro[5]))
            query.bindValue(":direcli", None if not (str(registro[6])) else str(registro[6]))
            query.bindValue(":provcli", None if not (str(registro[7])) else str(registro[7]))
            query.bindValue(":municli", None if not (str(registro[8])) else str(registro[8]))
            query.bindValue(":bajacli", None if not (str(registro[9])) else str(registro[9]))


            if query.exec() and query.numRowsAffected()>0:
                print(query.numRowsAffected())
                return True
            else:
                return False
        except Exception as e:
            print("Fallo cargando modificacion en la bd:" + e)

    def bajaCliente(datos):
        try:

            query = QtSql.QSqlQuery()
            query.prepare("UPDATE clientes SET bajacli =:bajacli WHERE dnicli = :dni")
            query.bindValue(":dni", str(datos[0]).strip())
            query.bindValue(":bajacli", str(datos[1]))

            if query.exec() and query.numRowsAffected()>0:
                return True
            else:
                return False

        except Exception as e:
            print("Error baja cliente bd",e)


    '''CONEXIONES PROPIEDADES'''
    def altaTipoPropiedad(tipoPropiedad):
        try:

            query = QtSql.QSqlQuery()
            query.prepare("INSERT into tipoprop"
                          " VALUES (:tipoPropiedad)")

            #if str empty =null
            # null if not str(nuevoCli[0]) else str(nuevoCli[0])
            query.bindValue(":tipoPropiedad", None if not tipoPropiedad else tipoPropiedad)

            if query.exec():
                print("Tipo propiedad añadida")
                return True
            else:
                return False
        except Exception as e:
            print("Error altaTipoPropiedad (conexion.py): ",e)

    def bajaTipoPropiedad(tipoPropiedad):
        try:

            query = QtSql.QSqlQuery()
            query.prepare("DELETE FROM tipoprop"
                          " WHERE tipo =:tipoPropiedad")

            query.bindValue(":tipoPropiedad", tipoPropiedad)

            if query.exec() and query.numRowsAffected()>0:
                print("Tipo propiedad eliminada")
                return True
            else:
                return False
        except Exception as e:
            print("Error bajaTipoPropiedad (conexion.py): ",e)

    def listaTipoPropiedad(self):
        listaTipoProp = []
        query = QtSql.QSqlQuery()
        query.prepare("SELECT * FROM tipoprop")

        if query.exec():
            while query.next():
                listaTipoProp.append(query.value(0))

        return listaTipoProp

    def altaPropiedad(propiedad):
        try:
            query = QtSql.QSqlQuery()
            query.prepare("Insert into propiedades (altaprop, bajaprop, dirprop, provprop, muniprop, cpprop,"
                          "tipoprop, habprop, banprop, superprop, prealquiprop, prevenprop,"
                          "obserprop, tipooperprop, estadoprop, nomeprop, movilprop) VALUES "
                          "(:altaprop, :bajaprop, :dirprop, :provprop, :muniprop, :cpprop,"
                          ":tipoprop, :habprop, :banprop, :superprop, :prealquiprop, :prevenprop,"
                          ":obserprop, :tipooperprop, :estadoprop, :nomeprop, :movilprop)")

            query.bindValue(":altaprop", None if not str(propiedad[0]) else str(propiedad[0]))
            query.bindValue(":bajaprop", None if not str(propiedad[1]) else str(propiedad[1]))
            query.bindValue(":dirprop", None if not str(propiedad[2]) else str(propiedad[2]))
            query.bindValue(":provprop", None if not str(propiedad[3]) else str(propiedad[3]))
            query.bindValue(":muniprop", None if not str(propiedad[4]) else str(propiedad[4]))
            query.bindValue(":cpprop", None if not str(propiedad[5]) else str(propiedad[5]))
            query.bindValue(":tipoprop", None if not str(propiedad[6]) else str(propiedad[6]))
            query.bindValue(":habprop", None if not str(propiedad[7]) else str(propiedad[7]))
            query.bindValue(":banprop", None if not str(propiedad[8]) else str(propiedad[8]))
            query.bindValue(":superprop", None if not str(propiedad[9]) else str(propiedad[9]))
            query.bindValue(":prealquiprop", None if not str(propiedad[10]) else str(propiedad[10]))
            query.bindValue(":prevenprop", None if not str(propiedad[11]) else str(propiedad[11]))
            query.bindValue(":obserprop", None if not str(propiedad[12]) else str(propiedad[12]))
            query.bindValue(":tipooperprop", None if not str(propiedad[13]) else str(propiedad[13]))
            query.bindValue(":estadoprop", None if not str(propiedad[14]) else str(propiedad[14]))
            query.bindValue(":nomeprop", None if not str(propiedad[15]) else str(propiedad[15]))
            query.bindValue(":movilprop", None if not str(propiedad[16]) else str(propiedad[16]))

            if query.exec():
                print("Propiedad añadida")
                return True
            else:
                return False
        except Exception as e:
            print("Error altaPropiedad (conexion.py): ",e)

    def listadoPropiedades(self):
        try:
            listado=[]
            if var.ui.chkHistoricoProp.isChecked(): #Si esta chekeado muestra to-do
                query = QtSql.QSqlQuery()
                query.prepare("SELECT * FROM propiedades ORDER BY codigo ASC")

                if query.exec():
                    while query.next():
                        fila = [query.value(i) for i in range(query.record().count())]
                        listado.append(fila)
                return listado
            else:
                query = QtSql.QSqlQuery()
                query.prepare("SELECT * FROM propiedades WHERE bajaprop IS null ORDER BY codigo ASC")

                if query.exec():
                    while query.next():
                        fila = [query.value(i) for i in range(query.record().count())]
                        listado.append(fila)
                return listado
        except Exception as e:
            print("Error recuperando el listado de propiedades (conexion.py)",e)

    def datosOnePropiedad(codigo):
        try:
            registro = []
            query = QtSql.QSqlQuery()
            query.prepare("SELECT * FROM propiedades WHERE codigo = :codigoProp")

            query.bindValue(":codigoProp",str(codigo).strip())

            if query.exec():
                while query.next():
                   for i in range(query.record().count()):
                    registro.append(str(query.value(i)))

            return registro

        except Exception as e:
            print("Error recuperando datos de propiedad (conexion.py)",e)

    def modifPropiedad(registro):
        try:

            query=QtSql.QSqlQuery()
            query.prepare("UPDATE propiedades SET altaprop=:altaprop, bajaprop=:bajaprop, dirprop=:dirprop, provprop=:provprop"
                          ", muniprop=:muniprop, cpprop=:cpprop,tipoprop=:tipoprop, habprop=:habprop,"
                          " banprop=:banprop, superprop=:superprop, prealquiprop=:prealquiprop, prevenprop=:prevenprop,"
                          "obserprop=:obserprop, tipooperprop=:tipooperprop, estadoprop=:estadoprop, nomeprop=:nomeprop,"
                          "movilprop=:movilprop WHERE codigo = :codigoProp")

            query.bindValue(":codigoProp", str(registro[0]))
            registro=registro[1:]
            query.bindValue(":altaprop", None if not str(registro[0]) else str(registro[0]))
            query.bindValue(":bajaprop", None if not str(registro[1]) else str(registro[1]))
            query.bindValue(":dirprop", None if not str(registro[2]) else str(registro[2]))
            query.bindValue(":provprop", None if not str(registro[3]) else str(registro[3]))
            query.bindValue(":muniprop", None if not str(registro[4]) else str(registro[4]))
            query.bindValue(":cpprop", None if not str(registro[5]) else str(registro[5]))
            query.bindValue(":tipoprop", None if not str(registro[6]) else str(registro[6]))
            query.bindValue(":habprop", None if not str(registro[7]) else str(registro[7]))
            query.bindValue(":banprop", None if not str(registro[8]) else str(registro[8]))
            query.bindValue(":superprop", None if not str(registro[9]) else str(registro[9]))
            query.bindValue(":prealquiprop", None if not str(registro[10]) else str(registro[10]))
            query.bindValue(":prevenprop", None if not str(registro[11]) else str(registro[11]))
            query.bindValue(":obserprop", None if not str(registro[12]) else str(registro[12]))
            query.bindValue(":tipooperprop", None if not str(registro[13]) else str(registro[13]))
            query.bindValue(":estadoprop", None if not str(registro[14]) else str(registro[14]))
            query.bindValue(":nomeprop", None if not str(registro[15]) else str(registro[15]))
            query.bindValue(":movilprop", None if not str(registro[16]) else str(registro[16]))

            if query.exec() and query.numRowsAffected()>0:
                print(query.numRowsAffected())
                return True
            else:
                return False
        except Exception as e:
            print("Fallo cargando modificacion de propieded en la bd (conexion.py):", e)