import os
from datetime import datetime
from idlelib import query

from PyQt6 import QtSql, QtWidgets
from PyQt6.QtGui import QIcon
from PyQt6.uic.properties import QtCore

import eventos
import var


class Conexion:

    """
    @staticmethod
    méto-do de una clase que no depende de una instancia específica de esa clase.
    Se puede llamarlo directamente a través de la clase, sin necesidad de crear un objeto de esa clase.
    Es útil en comportamientos o funcionalidades que son más a una clase en general que a una instancia en particular.

    """

    @staticmethod
    def db_conexion(self):
        """

        :param self: None
        :type self: None
        :return: False or True
        :rtype: bool
        """
        # Verifica si el archivo de base de datos existe
        if not os.path.isfile('bbdd.sqlite'):
            eventos.Eventos.alertMaker("Critical","Error","El archivo de la base de datos no existe.")
            #QtWidgets.QMessageBox.critical(None, 'Error', 'El archivo de la base de datos no existe.',
             #                              QtWidgets.QMessageBox.StandardButton.Cancel)
            return False
        # Crear la conexión con la base de datos SQLite
        db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('bbdd.sqlite')

        if db.open():
            # Verificar si la base de datos contiene tablas
            query = QtSql.QSqlQuery()
            query.exec("SELECT name FROM sqlite_master WHERE type='table';")

            if not query.next():  # Si no hay tablas
                eventos.Eventos.alertMaker("Critical", "Error", "Base de datos vacía o no válida")
                return False
            else:
                eventos.Eventos.alertMaker("Information", "Aviso", "Conexión Base de Datos realizada")
                return True
        else:
            eventos.Eventos.alertMaker("Critical", "Error", "No se pudo abrir la base de datos")
            return False

    @staticmethod
    def listaProv(self):
        """

        :param self: None
        :type self: None
        :return: lista de provincias
        :rtype: list

        Metodo que obtiene una lista con todos las provincias en la bd

        """
        listaprov=[]
        query= QtSql.QSqlQuery()
        query.prepare("SELECT * FROM provincias")

        if query.exec():
            while query.next():
                listaprov.append(query.value(1))

        return listaprov

    @staticmethod
    def listaMuni(provincia):
        """

        :param provincia: nombre de la provincia
        :type provincia: str
        :return: lista de municipios de la provincia
        :rtype: list

        Devuelve una lista con los municipios de la provincia

        """
        listamunicipios = []
        query = QtSql.QSqlQuery()
        query.prepare("SELECT * FROM municipios where idprov = (select idprov from provincias where provincia = :provincia)")
        query.bindValue(":provincia", provincia)
        if query.exec():
            while query.next():
                listamunicipios.append(query.value(1))
        return listamunicipios

    @staticmethod
    def listAllMuni():
        """

        :param: None
        :type: None
        :return: lista de municipios
        :rtype: list

        Devuelve una lista con todos los municipios de la bd

        """
        listamunicipios = []
        query = QtSql.QSqlQuery()
        query.prepare("SELECT * FROM municipios")

        if query.exec():
            while query.next():
                listamunicipios.append(query.value(1))
        else:
            print("Query execution failed:", query.lastError().text())
        return listamunicipios

    @staticmethod
    def listaMuniConPropiedades():
        try:
            listamunicipios = []
            query = QtSql.QSqlQuery()
            query.prepare("SELECT muniprop FROM propiedades GROUP BY muniprop")

            if query.exec():
                while query.next():
                    listamunicipios.append(query.value(0))
            else:
                print("Query execution failed:", query.lastError().text())
            return listamunicipios

        except Exception as e:
            print("Error recuperando listado de municipios con propiedades",e)

    '''
    CONEXIONES CLIENTES
    
    '''

    def altaCliente(nuevoCli):
        """

        :param nuevoCli: lista con datos de cliente
        :type nuevoCli: list
        :return: true or false
        :rtype: bool

        Metodo que inserta un nuevo registro cliente en la bd

        """
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
        """

        :param self: None
        :type self: None
        :return: listado de listas de datos de clientes
        :rtype: list

        Devuelve una lista con las listas de datos de aqueyos clientes que coincidan con los criterios.
        Dependiendo de si el checkbox Historico sea true o false se incluiran todos los clientes o solo aquellos sin fecha de baja respectivamente
        """
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
        """

        :param dni: DNI de un cliente
        :type dni: str
        :return: listado de datos de un cliente
        :rtype: list

        Devuelve los datos del cliente cuyo dni coincida con el dni proporcionado

        """
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
        """

        :param registro: lista de datos de un cliente
        :type registro: list
        :return: True or False
        :rtype: bool

        Recoge los datos de un cliente y los modifica en el registro adecuado segun el DNI (PK).
        Devuelve True si la modificación ha sido exitosa y False en caso contrario

        """
        try:
            query=QtSql.QSqlQuery()
            query.prepare("UPDATE clientes SET altacli =:altacli, apecli = :apecli, nomecli = :nomecli, emailcli = :emailcli, "
                          " movilcli = :movilcli, direcli = :direcli, provcli = :provcli, municli = :municli, bajacli = :bajacli "
                          " WHERE dnicli = :dni")

            query.bindValue(":dni", None if not str(registro[0]) else str(registro[0]))
            query.bindValue(":altacli", None if not str(registro[1]) else str(registro[1]))
            query.bindValue(":apecli", None if not str(registro[2]) else str(registro[2]))
            query.bindValue(":nomecli", None if not str(registro[3]) else str(registro[3]))
            query.bindValue(":emailcli", None if not str(registro[4]) else str(registro[4]))
            query.bindValue(":movilcli", None if not str(registro[5]) else str(registro[5]))
            query.bindValue(":direcli", None if not str(registro[6]) else str(registro[6]))
            query.bindValue(":provcli", None if not str(registro[7]) else str(registro[7]))
            query.bindValue(":municli", None if not str(registro[8]) else str(registro[8]))
            query.bindValue(":bajacli", None if not str(registro[9]) else str(registro[9]))


            if query.exec():
                if query.numRowsAffected()>0:
                    print(query.numRowsAffected())
                    return True
                else:
                    print("Query executed but no rows affected")
                    return True
            else:
                print("Error executing query:", query.lastError().text())
                return False
        except Exception as e:
            print("Fallo cargando modificacion en la bd:" + str(e))

    def bajaCliente(datos):
        """

        :param datos: lista de datos (dni, fecha de baja)
        :type datos: list
        :return: True or False
        :rtype: bool

        Modifica la fecha de baja del cliente que coincida con el dni proporcionado.
        No elimina el registro de la bd

        """
        try:

            query = QtSql.QSqlQuery()
            query.prepare("UPDATE clientes SET bajacli =:bajacli WHERE dnicli = :dni")
            query.bindValue(":dni", str(datos[0]).strip())
            query.bindValue(":bajacli", None if not str(datos[1]) else str(datos[1]))

            if query.exec() and query.numRowsAffected()>0:
                return True
            else:
                return False

        except Exception as e:
            print("Error baja cliente bd",e)


    '''
    CONEXIONES PROPIEDADES
    
    '''
    def altaTipoPropiedad(tipoPropiedad):
        """

        :param tipoPropiedad: lista de datos (dni, fecha de baja)
        :type tipoPropiedad: list
        :return:
        :rtype:
        """
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

    @staticmethod
    def listaTipoPropiedad():
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
                          "obserprop, nomeprop, movilprop, tipooperprop, estadoprop) VALUES "
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
            query.bindValue(":nomeprop", None if not str(propiedad[13]) else str(propiedad[15]))
            query.bindValue(":movilprop", None if not str(propiedad[14]) else str(propiedad[16]))
            query.bindValue(":tipooperprop", None if not str(propiedad[15]) else str(propiedad[13]))
            query.bindValue(":estadoprop", None if not str(propiedad[16]) else str(propiedad[14]))


            if query.exec():
                print("Propiedad añadida")
                return True
            else:
                return False
        except Exception as e:
            print("Error altaPropiedad (conexion.py): ",e)

    def listadoAllPropiedades(self):
        try:
            listado=[]

            query = QtSql.QSqlQuery()
            query.prepare("SELECT * FROM propiedades ORDER BY codigo ASC")
            if query.exec():
                while query.next():
                    fila = [query.value(i) for i in range(query.record().count())]
                    listado.append(fila)
            return listado

        except Exception as e:
            print("Error recuperando el listado de propiedades (conexion.py)",e)

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

    def listaPropiedadesByTipo(self,tipoPropiedad):
        try:
            listado = []
            if var.ui.chkHistoricoProp.isChecked():  # Si esta chekeado muestra to-do
                query = QtSql.QSqlQuery()
                query.prepare("SELECT * FROM propiedades WHERE tipoprop = :tipoprop ORDER BY codigo ASC")

                query.bindValue(":tipoprop", tipoPropiedad)

                if query.exec():
                    while query.next():
                        fila = [query.value(i) for i in range(query.record().count())]
                        listado.append(fila)
                return listado
            else:
                query = QtSql.QSqlQuery()
                query.prepare("SELECT * FROM propiedades WHERE bajaprop IS null and tipoprop = :tipoprop ORDER BY codigo ASC")

                query.bindValue(":tipoprop", tipoPropiedad)

                if query.exec():
                    while query.next():
                        fila = [query.value(i) for i in range(query.record().count())]
                        listado.append(fila)
                return listado
        except Exception as e:
            print("Error lista Propiedades por tipo (conexion.py): ",e)

    @staticmethod
    def listaPropiedadesByMuni(muni):
        try:
            listado = []
            if var.ui.chkHistoricoProp.isChecked():  # Si esta chekeado muestra to-do
                query = QtSql.QSqlQuery()
                query.prepare("SELECT * FROM propiedades WHERE muniprop = :muniprop ORDER BY codigo ASC")

                query.bindValue(":muniprop", muni)

                if query.exec():
                    while query.next():
                        fila = [query.value(i) for i in range(query.record().count())]
                        listado.append(fila)
                return listado
            else:
                query = QtSql.QSqlQuery()
                query.prepare(
                    "SELECT * FROM propiedades WHERE bajaprop IS null and muniprop = :muniprop ORDER BY codigo ASC")

                query.bindValue(":muniprop", muni)

                if query.exec():
                    while query.next():
                        fila = [query.value(i) for i in range(query.record().count())]
                        listado.append(fila)
                return listado
        except Exception as e:
            print("Error lista Propiedades por municipio (conexion.py): ",e)

    def listaPropiedadesByTipoMuni(self,tipo,muni):
        try:
            listado = []
            if var.ui.chkHistoricoProp.isChecked():  # Si esta chekeado muestra to-do
                query = QtSql.QSqlQuery()
                query.prepare("SELECT * FROM propiedades WHERE tipoprop = :tipoprop and muniprop = :muniprop ORDER BY codigo ASC")

                query.bindValue(":muniprop", muni)
                query.bindValue(":tipoprop", tipo)

                if query.exec():
                    while query.next():
                        fila = [query.value(i) for i in range(query.record().count())]
                        listado.append(fila)
                return listado
            else:
                query = QtSql.QSqlQuery()
                query.prepare(
                    "SELECT * FROM propiedades WHERE bajaprop IS null and tipoprop = :tipoprop and muniprop = :muniprop ORDER BY codigo ASC")

                query.bindValue(":muniprop", muni)
                query.bindValue(":tipoprop", tipo)

                if query.exec():
                    while query.next():
                        fila = [query.value(i) for i in range(query.record().count())]
                        listado.append(fila)
                return listado
        except Exception as e:
            print("Error lista Propiedades por Tipo y Municipio (conexion.py): ",e)

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
                          "obserprop=:obserprop, nomeprop=:nomeprop, movilprop=:movilprop,"
                          " tipooperprop=:tipooperprop, estadoprop=:estadoprop WHERE codigo = :codigoProp")

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
            query.bindValue(":nomeprop", None if not str(registro[13]) else str(registro[13]))
            query.bindValue(":movilprop", None if not str(registro[14]) else str(registro[14]))
            query.bindValue(":tipooperprop", None if not str(registro[15]) else str(registro[15]))
            query.bindValue(":estadoprop", None if not str(registro[16]) else str(registro[16]))

            if query.exec() and query.numRowsAffected()>0:
                print(query.numRowsAffected())
                return True
            else:
                return False
        except Exception as e:
            print("Fallo cargando modificacion de propieded en la bd (conexion.py):", e)

    def bajaPropiedad(datos):
        try:

            query = QtSql.QSqlQuery()
            query.prepare("UPDATE propiedades SET bajaprop =:bajaprop WHERE codigo = :codigo")
            query.bindValue(":codigo", str(datos[0]).strip())
            query.bindValue(":bajaprop", str(datos[1]))

            if query.exec() and query.numRowsAffected()>0:
                return True
            else:
                return False

        except Exception as e:
            print("Error baja propiedad bd (conexion.py): ",e)

    @staticmethod
    def getPropiedadById(id):
        try:
            registro = []
            query = QtSql.QSqlQuery()
            query.prepare(
                "select p.codigo, p.dirprop, p.muniprop, p.tipoprop, p.prevenprop from propiedades p where codigo = :cod")

            query.bindValue(":cod", int(id))

            if query.exec():
                while query.next():
                    for i in range(query.record().count()):
                        registro.append(str(query.value(i)))
            else:
                print("Error executing query: ", query.lastError().text())
                return False

            return registro

        except Exception as e:
            print("Error recuperando datos de propiedad by id (conexion.py): ", e)

    @staticmethod
    def setEstadoVendido(codigoProp,fechabaja):
        try:

            query=QtSql.QSqlQuery()
            query.prepare("UPDATE propiedades SET estadoprop=:estadoprop, bajaprop=:bajaprop WHERE codigo = :codigoProp")

            query.bindValue(":codigoProp", codigoProp)
            query.bindValue(":estadoprop", "Vendido")
            query.bindValue(":bajaprop", str(fechabaja))

            if query.exec() and query.numRowsAffected()>0:
                print(query.numRowsAffected())
                return True
            else:
                return False
        except Exception as e:
            print("Fallo cargando modificacion de propieded en la bd (conexion.py):", e)

    @staticmethod
    def setEstadoDisponible(codigoProp):
        try:

            query=QtSql.QSqlQuery()
            query.prepare("UPDATE propiedades SET estadoprop=:estadoprop, bajaprop=:bajaprop WHERE codigo = :codigoProp")

            query.bindValue(":codigoProp", codigoProp)
            query.bindValue(":estadoprop", "Disponible")
            query.bindValue(":bajaprop", None)

            if query.exec() and query.numRowsAffected()>0:
                print(query.numRowsAffected())
                return True
            else:
                return False
        except Exception as e:
            print("Fallo cargando modificacion de propieded en la bd (conexion.py):", e)

    @staticmethod
    def isDisponible(codigo):
        try:

            query=QtSql.QSqlQuery()
            query.prepare("select * from propiedades where codigo=:codigo AND estadoprop = 'Vendido'")

            query.bindValue(":codigo", codigo)

            if query.exec():
                return query.next()  # Returns True if there's at least one match, False otherwise
            return False
        except Exception as e:
            print("Fallo recuperando disponibilidad en la bd (conexion.py):", e)


    '''''
    CONEXIONES VENDEDORES
    
    '''

    def altaVendedores(nuevoVendedor):
        try:

            query = QtSql.QSqlQuery()
            query.prepare("INSERT into vendedores (dniVendedor, nombreVendedor, altaVendedor, bajaVendedor, movilVendedor, emailVendedor, delegacionVendedor)"
                          " VALUES (:dniVendedor, :nombreVendedor, :altaVendedor, :bajaVendedor, :movilVendedor, :emailVendedor, :delegacionVendedor)")

            query.bindValue(":dniVendedor", None if not str(nuevoVendedor[0]) else str(nuevoVendedor[0]))
            query.bindValue(":nombreVendedor", None if not str(nuevoVendedor[1]) else str(nuevoVendedor[1]))
            query.bindValue(":altaVendedor", None if not str(nuevoVendedor[2]) else str(nuevoVendedor[2]))
            query.bindValue(":bajaVendedor", None if not str(nuevoVendedor[3]) else str(nuevoVendedor[3]))
            query.bindValue(":movilVendedor", None if not str(nuevoVendedor[4]) else str(nuevoVendedor[4]))
            query.bindValue(":emailVendedor", None if not str(nuevoVendedor[5]) else str(nuevoVendedor[5]))
            query.bindValue(":delegacionVendedor", None if not str(nuevoVendedor[6]) else str(nuevoVendedor[6]))


            if query.exec():
                print("Vendedor añadido")
                return True
            else:
                print("Error executing query:", query.lastError().text())
                return False
        except Exception as e:
            print("Error alta vendedor (conexion.py)",e)

    def listadoVendedores(self):
        try:
            listado=[]

            if var.ui.chkHistoricoVendedores.isChecked():
                query = QtSql.QSqlQuery()
                #Where fecha baja = null
                query.prepare("SELECT * FROM vendedores ORDER BY idVendedor ASC")

                if query.exec():
                    while query.next():
                        fila = [query.value(i) for i in range(query.record().count())]
                        listado.append(fila)
                return listado
            else:
                query = QtSql.QSqlQuery()
                # Where fecha baja = null
                query.prepare("SELECT * FROM vendedores WHERE bajaVendedor IS null ORDER BY idVendedor ASC")

                if query.exec():
                    while query.next():
                        fila = [query.value(i) for i in range(query.record().count())]
                        listado.append(fila)
                return listado
        except Exception as e:
            print("Error recuperando el listado de vendedores",e)

    def datosOneVendedor(id):
        try:
            registro = []
            query = QtSql.QSqlQuery()
            query.prepare("SELECT * FROM vendedores WHERE idVendedor = :idVendedor")

            query.bindValue(":idVendedor",str(id).strip())

            if query.exec():
                while query.next():
                   for i in range(query.record().count()):
                    registro.append(str(query.value(i)))

            return registro

        except Exception as e:
            print("Error recuperando datos de vensedor",e)

    def modifVendedor(registro):
        try:
            qq = QtSql.QSqlQuery()
            qq.prepare("SELECT * FROM vendedores WHERE idVendedor = :idVendedor")

            qq.bindValue(":idVendedor", registro[0])

            if qq.exec():
                if qq.next():
                    dniAntiguo = qq.value(1)
            else:
                print("SQL Error:", qq.lastError().text())

            if dniAntiguo != str(registro[1]):
                print("DNI Cambiado",str(registro[1]))
                eventos.Eventos.alertMaker("Critical", "Aviso","No puedes modificar el dni de un vendedor")
                return


            query=QtSql.QSqlQuery()
            query.prepare("UPDATE vendedores SET nombreVendedor = :nombreVendedor,"
                          " altaVendedor = :altaVendedor, bajaVendedor = :bajaVendedor, "
                          "movilVendedor = :movilVendedor, emailVendedor = :emailVendedor,"
                          " delegacionVendedor = :delegacionVendedor"
                          " WHERE idVendedor = :idVendedor")

            query.bindValue(":idVendedor", None if not str(registro[0]) else str(registro[0]))
            query.bindValue(":nombreVendedor", None if not str(registro[2]) else str(registro[2]))
            query.bindValue(":altaVendedor", None if not str(registro[3]) else str(registro[3]))
            query.bindValue(":bajaVendedor", None if not str(registro[4]) else str(registro[4]))
            query.bindValue(":movilVendedor", None if not str(registro[5]) else str(registro[5]))
            query.bindValue(":emailVendedor", None if not str(registro[6]) else str(registro[6]))
            query.bindValue(":delegacionVendedor", None if not str(registro[7]) else str(registro[7]))


            if query.exec():
                if query.numRowsAffected()>0:
                    print('Rows affected: ',query.numRowsAffected())
                    return True
                else:
                    print("Query executed but no rows affected")
                    return True
            else:
                print("Error executing query (modif vendedor):", query.lastError().text())

                return False
        except Exception as e:
            print("Fallo cargando modificacion de vendedor en la bd:" + str(e))

    def bajaVendedor(datos):
        try:
            query = QtSql.QSqlQuery()
            query.prepare("UPDATE vendedores SET bajaVendedor = :bajaVendedor WHERE idVendedor = :idVendedor")
            query.bindValue(":idVendedor", str(datos).strip())
            dia = datetime.now().day
            mes = datetime.now().month
            ano = datetime.now().year
            fecha = str(dia)+"/"+str(mes)+"/"+str(ano)
            #print(fecha)
            query.bindValue(":bajaVendedor", fecha)

            if query.exec() and query.numRowsAffected()>0:
                return True
            else:
                print("Error executing query:", query.lastError().text())
                return False

        except Exception as e:
            print("Error baja vendedor bd",e)

    def getAllDniVendedores(self):
        try:
            dnis=[]

            query = QtSql.QSqlQuery()
            #Where fecha baja = null
            query.prepare("SELECT dniVendedor FROM vendedores ORDER BY idVendedor ASC")

            if query.exec():
                while query.next():
                    fila = [query.value(i) for i in range(query.record().count())]
                    dnis.append(fila[0])
                #print(dnis)
            return dnis

        except Exception as e:
            print("Error recuperando el listado de vendedores",e)

    def datosVendedorByMovil(movil):
        try:
            registro = []
            query = QtSql.QSqlQuery()
            query.prepare("SELECT * FROM vendedores WHERE movilVendedor = :movilVendedor")

            query.bindValue(":movilVendedor",str(movil).strip())

            if query.exec():
                while query.next():
                   for i in range(query.record().count()):
                    registro.append(str(query.value(i)))

            return registro

        except Exception as e:
            print("Error recuperando datos de vensedor",e)

    def listAllVendedores(self):
        try:
            registro = []
            query = QtSql.QSqlQuery()
            query.prepare("SELECT * FROM vendedores ")

            if query.exec():
                while query.next():
                    fila = [query.value(i) for i in range(query.record().count())]
                    registro.append(fila)
            return registro

        except Exception as e:
            print("Error recuperando datos de vensedor",e)

    @staticmethod
    def getIdNameDniFromVendedores():
        try:
            registro = []
            query = QtSql.QSqlQuery()
            query.prepare("select idVendedor,nombreVendedor, dniVendedor from vendedores")

            if query.exec():
                while query.next():
                    fila = [query.value(i) for i in range(query.record().count())]
                    print(fila)
                    registro.append(fila)
            else:
                print("Error executing query:", query.lastError().text())
                return False

            return registro

        except Exception as e:
            print("Error recuperando datos id, nombre y dni de vendedor", e)

    '''
    CONEXIONES VENTAS
    
    '''
    @staticmethod
    def altaFactura(factura):
        try:
            print("datos dactura a dar de alta: ",factura)
            query = QtSql.QSqlQuery()
            query.prepare("INSERT INTO facturas (fechaFactura,dniFactura) VALUES (:fechaFactura,:dniFactura)")

            query.bindValue(":fechaFactura", factura[0])
            query.bindValue(":dniFactura", factura[1].strip())

            if query.exec():
                return True
            else:
                print("Error executing query: ", query.lastError().text())
                return False
        except Exception as e:
            print("Error alta factura (conexion.py): ",e)

    @staticmethod
    def listaFacturas():
        try:
            listado=[]
            query = QtSql.QSqlQuery()
            query.prepare("Select * FROM facturas")

            if query.exec():
                while query.next():
                    fila = [query.value(i) for i in range(query.record().count())]
                    listado.append(fila)
                return listado
            else:
                print("Error executing query: ", query.lastError().text())
                return False
        except Exception as e:
            print("Error listado facturas (conexion.py): ", e)

    @staticmethod
    def eliminarFactura(idFactura):
        try:
            query = QtSql.QSqlQuery()
            query.prepare("DELETE FROM facturas WHERE idFactura = :idFactura")
            query.bindValue(":idFactura", idFactura)

            if query.exec() and query.numRowsAffected()>0:
                return True
            else:
                print("Error executing query eliminarFactura: ", query.lastError().text())
                return False

        except Exception as e:
            print("Error eliminar factura bd (conexion.py)",e)

    @staticmethod
    def getVentasFromFactura(idFactura):
        try:
            listado=[]
            query = QtSql.QSqlQuery()
            query.prepare("Select * FROM ventas WHERE idFactura = :idFactura")
            query.bindValue(":idFactura", idFactura)

            if query.exec():
                while query.next():
                   fila = [query.value(i) for i in range(query.record().count())]
                   listado.append(fila)

                return listado
            else:
                print("Error executing query: ", query.lastError().text())
                return False
        except Exception as e:
            print("Error listado ventas por factura (conexion.py): ", e)

    @staticmethod
    def getNextIdFactura():
        query = QtSql.QSqlQuery()
        query.prepare("SELECT Max(idFactura) FROM facturas")

        if query.exec():
            query.next()
            return query.value(0)+1
        else:
            print("Error executing query: ", query.lastError().text())
            return False

    @staticmethod
    def getFacturaById(idFactura):
        try:
            registro = []
            query = QtSql.QSqlQuery()
            query.prepare("select f.idFactura, f.fechaFactura, f.dniFactura ,c.nomecli, c.apecli from facturas as f INNER JOIN clientes as c on f.dniFactura=c.dnicli where idFactura = :idFactura")

            query.bindValue(":idFactura", str(idFactura).strip())

            if query.exec():
                while query.next():
                    for i in range(query.record().count()):
                        registro.append(str(query.value(i)))
            else:
                print("Error executing query: ", query.lastError().text())
                return False

            return registro

        except Exception as e:
            print("Error recuperando datos de factura (conexion.py): ", e)

    @staticmethod
    def altaVenta(venta):
        try:

            query = QtSql.QSqlQuery()
            query.prepare("insert into ventas (idFactura,idPropiedad,idVendedor) values (:idFactura,:idPropiedad,:idVendedor)")

            query.bindValue(":idFactura", venta[0])
            query.bindValue(":idPropiedad", venta[1])
            query.bindValue(":idVendedor", venta[2])

            if query.exec():
                return True
            else:
                print("Error executing query: ", query.lastError().text())
                return False
        except Exception as e:
            print("Error alta factura (conexion.py): ", e)

    @staticmethod
    def eliminarVenta(idVenta):
        try:
            query = QtSql.QSqlQuery()
            query.prepare("DELETE FROM ventas WHERE idVenta = :idVenta")
            query.bindValue(":idVenta", idVenta)

            if query.exec() and query.numRowsAffected() > 0:
                return True
            else:
                print("Error executing query eliminarVenta: ", query.lastError().text())
                return False

        except Exception as e:
            print("Error eliminar factura bd (conexion.py)", e)


    '''
    CONEXIONES ALQUILERES
    '''

    @staticmethod
    def listaContratos():
        try:
            listado = []
            query = QtSql.QSqlQuery()
            query.prepare("Select * FROM contratos")

            if query.exec():
                while query.next():
                    fila = [query.value(i) for i in range(query.record().count())]
                    listado.append(fila)
                return listado
            else:
                print("Error executing query: ", query.lastError().text())
                return False
        except Exception as e:
            print("Error listado contratos (conexion.py): ", e)

    @staticmethod
    def getContratoById(idContrato):
        try:
            registro = []
            query = QtSql.QSqlQuery()
            query.prepare(
                "SELECT con.idContrato, con.idVendedor, con.fechaFirma, con.fechaInicio, con.fechaFin, p.codigo, p.dirprop, p.muniprop, p.cpprop, cli.dnicli, cli.nomecli, cli.apecli from contratos as con INNER join clientes as cli on con.idCliente = cli.dnicli INNER join propiedades as p on con.idPropiedad = p.codigo where con.idContrato = :idContrato")

            query.bindValue(":idContrato", str(idContrato).strip())

            if query.exec():
                while query.next():
                    for i in range(query.record().count()):
                        registro.append(str(query.value(i)))
            else:
                print("Error executing query: ", query.lastError().text())
                return False

            return registro

        except Exception as e:
            print("Error recuperando datos de contrato (conexion.py): ", e)
