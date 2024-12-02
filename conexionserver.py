import mysql.connector
from mysql.connector import Error
import os
from PyQt6 import QtSql, QtWidgets

import var


class ConexionServer():
    def crear_conexion(self):

        try:
            conexion = mysql.connector.connect(
            host='192.168.10.66', # Cambia esto a la IP de tu servidor user='dam', # Usuario creado
            #host='192.168.1.49',
            user='dam',
            password='dam2425',
            database='bbdd',
            charset="utf8mb4",
            collation="utf8mb4_general_ci"  # Asegúrate de que aquí esté configurado
            # Contraseña del usuario database='bbdd' # Nombre de la base de datos
            )
            if conexion.is_connected():
                pass
                #print("Conexión exitosa a la base de datos")
            return conexion
        except Error as e:
            print(f"Error al conectar a la base de datos: {e}")
            return None
        return None

#--------PROVINCIAS Y MUNI------------------------------------------------------------------------------------------------------------

    @staticmethod
    def listaProv(self=None):
        listaprov = []
        conexion = ConexionServer().crear_conexion()

        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute("SELECT * FROM provincias")
                resultados = cursor.fetchall()
                for fila in resultados:
                    listaprov.append(fila[1])  # Asumiendo que el nombre de la provincia está en la segunda columna
                cursor.close()
                conexion.close()
            except Error as e:
                print(f"Error al ejecutar la consulta: {e}")
        return listaprov

    @staticmethod
    def listaMuniProv(provincia):
        try:
            conexion = ConexionServer().crear_conexion()
            listamunicipios = []
            cursor = conexion.cursor()
            cursor.execute(
                "SELECT * FROM municipios WHERE idprov = (SELECT idprov FROM provincias WHERE provincia = %s)",
                (provincia,)
            )
            resultados = cursor.fetchall()
            for fila in resultados:
                listamunicipios.append(fila[1])  # Asumiendo que el nombre de la provincia está en la segunda columna
            cursor.close()
            conexion.close()
            return listamunicipios
        except Exception as error:
            print("error lista muni", error)

    @staticmethod
    def listAllMuni():
        try:
            conexion = ConexionServer().crear_conexion()
            listamunicipios = []
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM municipios")

            resultados = cursor.fetchall()
            for fila in resultados:
                listamunicipios.append(fila[1])  # Asumiendo que el nombre de la provincia está en la segunda columna
            cursor.close()
            conexion.close()
            return listamunicipios
        except Exception as error:
            print("error lista muni", error)

#------CLIENTES------------------------------------------------------------------------------------------------------------------------------------------

    def listadoClientes(self):
        try:
            conexion = ConexionServer().crear_conexion()
            listadoclientes = []
            cursor = conexion.cursor()
            if var.ui.chkHistoricoCli.isChecked():
                cursor.execute("SELECT * FROM clientes ORDER BY apelcli, nomecli ASC")
                resultados = cursor.fetchall()
                # Procesar cada fila de los resultados
                for fila in resultados:
                    # Crear una lista con los valores de la fila
                    listadoclientes.append(list(fila))  # Convierte la tupla en una lista y la añade a listadoclientes

                # Cerrar el cursor y la conexión si no los necesitas más
                cursor.close()
                conexion.close()
                return listadoclientes
            else:
                cursor.execute("SELECT * FROM clientes WHERE bajacli IS null or bajacli = ' ' ORDER BY apelcli, nomecli ASC")
                resultados = cursor.fetchall()
                # Procesar cada fila de los resultados
                for fila in resultados:
                    # Crear una lista con los valores de la fila
                    listadoclientes.append(list(fila))  # Convierte la tupla en una lista y la añade a listadoclientes

                # Cerrar el cursor y la conexión si no los necesitas más
                cursor.close()
                conexion.close()
                return listadoclientes
        except Exception as e:
            print("error listado en conexion", e)

    def altaCliente(cliente):
        try:
            conexion = ConexionServer().crear_conexion()
            if conexion:
                cursor = conexion.cursor()
                # Definir la consulta de inserción
                query = """
                INSERT INTO clientes (dnicli, altacli, apelcli, nomecli, dircli, emailcli, movilcli, provcli, municli)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(query, cliente)  # Ejecutar la consulta pasando la lista directamente
                conexion.commit()  # Confirmar la transacción
                cursor.close()  # Cerrar el cursor y la conexión
                conexion.close()
                return True
        except Error as e:
            print(f"Error al insertar el cliente: {e}")

    def datosOneCliente(dni):
        registro = []  # Inicializa la lista para almacenar los datos del cliente
        try:
            conexion = ConexionServer().crear_conexion()
            if conexion:
                cursor = conexion.cursor()
                # Definir la consulta de selección
                query = '''SELECT * FROM clientes WHERE dnicli = %s'''  # Usa %s para el placeholder
                cursor.execute(query, (str(dni).strip(),))  # Pasar 'dni' como una tupla
                # Recuperar los datos de la consulta
                for row in cursor.fetchall():
                    registro.extend([str(col) for col in row])
            #print (registro)
                cursor.close()
                conexion.close()
            return registro

        except Exception as e:
            print("Error recogiendo datos de un cliente (conexionserver.py):", e)
            return None  # Devolver None en caso de error

    def modifCliente(registro):
        try:
            conexion = ConexionServer().crear_conexion()
            if conexion:
                cursor = conexion.cursor()
                query='''UPDATE clientes SET altacli = %s, apelcli = %s, nomecli = %s , emailcli = %s ,
                 movilcli = %s , dircli = %s , provcli = %s , municli = %s , bajacli = %s WHERE dnicli = %s '''
                cursor.execute(query, (
                None if not (str(registro[1])) else str(registro[1]),
                None if not (str(registro[2])) else str(registro[2]),
                None if not (str(registro[3])) else str(registro[3]),
                None if not str(registro[4]) else str(registro[4]),
                None if not (str(registro[5])) else str(registro[5]),
                None if not (str(registro[6])) else str(registro[6]),
                None if not (str(registro[7])) else str(registro[7]),
                None if not (str(registro[8])) else str(registro[8]),
                None if not (str(registro[9])) else str(registro[9]),
                None if not (str(registro[0])) else str(registro[0]),
                ))
                conexion.commit()
                if cursor.rowcount > 0:
                    cursor.close()
                    conexion.close()
                    return True
                else:
                    cursor.close()
                    conexion.close()
                    return False
        except Exception as e:
            print("Fallo cargando modificacion en la bd:" + str(e))

    def bajaCliente(datos):
        try:
            conexion = ConexionServer().crear_conexion()
            if conexion:
                cursor = conexion.cursor()
                query='''UPDATE clientes SET bajacli =%s WHERE dnicli = %s '''
                cursor.execute(query, (
                    str(datos[1]),
                    str(datos[0]).strip(),
                ))
                conexion.commit()
                if cursor.rowcount > 0:
                    cursor.close()
                    conexion.close()
                    return True
                else:
                    cursor.close()
                    conexion.close()
                    return False
        except Exception as e:
            print("Fallo cargando modificacion en la bd:" + str(e))

#--------TIPO PROPIEDADES-------------------------------------------------------------------------------------------------------

    def altaTipoPropiedad(tipoPropiedad):
        try:
            conexion = ConexionServer().crear_conexion()
            if conexion:
                cursor = conexion.cursor()
                query='''INSERT into tipoprop VALUES (%s)'''
                cursor.execute(query, (None if not tipoPropiedad else tipoPropiedad,))
                conexion.commit()
                if cursor.rowcount > 0:
                    cursor.close()
                    conexion.close()
                    return True
                else:
                    cursor.close()
                    conexion.close()
                    return False
        except Exception as e:
            print("Error altaTipoPropiedad (conexion.py): ",e)

    def bajaTipoPropiedad(tipoPropiedad):
        try:
            conexion = ConexionServer().crear_conexion()
            if conexion:
                cursor = conexion.cursor()
                query='''DELETE FROM tipoprop WHERE tipo = %s'''
                cursor.execute(query, (tipoPropiedad,))
                conexion.commit()
                if cursor.rowcount > 0:
                    cursor.close()
                    conexion.close()
                    return True
                else:
                    cursor.close()
                    conexion.close()
                    return False
        except Exception as e:
            print("Error bajaTipoPropiedad (conexion.py): ",e)

    @staticmethod
    def listaTipoPropiedad():
        listaTipoProp = []
        conexion = ConexionServer().crear_conexion()
        if conexion:
            cursor = conexion.cursor()
            query ='''SELECT * FROM tipoprop'''

            resultados = cursor.fetchall()
            # Procesar cada fila de los resultados
            for fila in resultados:
                # Crear una lista con los valores de la fila
                listaTipoProp.append(fila[0])  # Convierte la tupla en una lista y la añade a listadoclientes

            cursor.close()
            conexion.close()
            return listaTipoProp