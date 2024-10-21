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
            query.bindValue(":dnicli", str(nuevoCli[0]))
            query.bindValue(":altacli", str(nuevoCli[1]))
            query.bindValue(":apecli", str(nuevoCli[2]))
            query.bindValue(":nomecli", str(nuevoCli[3]))
            query.bindValue(":emailcli", None if not str(nuevoCli[4]) else str(nuevoCli[4]))
            query.bindValue(":movilcli", str(nuevoCli[5]))
            query.bindValue(":direcli", str(nuevoCli[6]))
            query.bindValue(":provcli", str(nuevoCli[7]))
            query.bindValue(":municli", str(nuevoCli[8]))
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
            if var.historico==0:
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

            query.bindValue(":dni", str(registro[0]))
            query.bindValue(":altacli", str(registro[1]))
            query.bindValue(":apecli", str(registro[2]))
            query.bindValue(":nomecli", str(registro[3]))
            query.bindValue(":emailcli", None if not str(registro[4]) else str(registro[4]))
            query.bindValue(":movilcli", str(registro[5]))
            query.bindValue(":direcli", str(registro[6]))
            query.bindValue(":provcli", str(registro[7]))
            query.bindValue(":municli", str(registro[8]))
            query.bindValue(":bajacli", None if not str(registro[9]) else str(registro[9]))

            print("PUTO")
            if query.exec():
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

            if query.exec():
                return True
            else:
                return False

        except Exception as e:
            print("Error baja cliente bd",e)


