import os
from idlelib import query

from PyQt6 import QtSql, QtWidgets
from PyQt6.QtGui import QIcon


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
            print(nuevoCli)
            query = QtSql.QSqlQuery()
            query.prepare("INSERT into clientes (dnicli,altacli,apecli,nomecli,emailcli,movilcli,direcli,provcli,municli)"
                          " VALUES (:dnicli,:altacli,:apecli,:nomecli,:emailcli,:movilcli,:direcli,:provcli,:municli)")

            '''Con este bucle si un campo se queda vacio si guarda como string vacia en vez de null, habría que arreglarlo
            fields = [
                ":dnicli", ":altacli", ":apecli", ":nomecli", ":emailcli",
                ":movilcli", ":direcli", ":provcli", ":municli"
            ]

            for field, value in zip(fields, nuevoCli):
                query.bindValue(field, str(value))'''

            query.bindValue(":dnicli", str(nuevoCli[0]))
            query.bindValue(":altacli", str(nuevoCli[1]))
            query.bindValue(":apecli", str(nuevoCli[2]))
            query.bindValue(":nomecli", str(nuevoCli[3]))
            query.bindValue(":emailcli", str(nuevoCli[4]))
            query.bindValue(":movilcli", str(nuevoCli[5]))
            query.bindValue(":direcli", str(nuevoCli[6]))
            query.bindValue(":provcli", str(nuevoCli[7]))
            query.bindValue(":municli", str(nuevoCli[8]))

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
            query = QtSql.QSqlQuery()
            query.prepare("SELECT * FROM clientes ORDER BY apecli, nomecli ASC")

            if query.exec():
                while query.next():
                    fila=[query.value(i) for i in range(query.record().count())]
                    listado.append(fila)
            return listado

        except Exception as e:
            print("Error recuperando el listado de clientes",e)