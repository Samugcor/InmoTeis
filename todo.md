validando los filtros para que el ususario no ponga cosas raras y pete todo

## 05/11/2024

- ✅Añadir propiedades. 
- ✅Eliminar propiedades.
- ✅Modificar propiedades.

- ✅Cargar propiedades en la tabla, campos: codigo, municipio, tipo propiedad habitaciones baño precio alquiler, precio venta tipo operacion. Los precios deben añadir el simbolo del euro (hardcode) y si estan vacios "- €".
Añade una columna para la baja de la propiedad.

- ✅Haz que funcione el historico.
- ✅Haz que el boton de borrar borre también el formulario de propiedades. (Estaria bien que borre dependiendo de la pestaña en la que estás).
- Nueva funcion de la barra de herramientas "lupa"

- Validar telefono propiedad
- Validar codigo postal

## 06/11/2024

- La nueva funcion "lupa" (buscar) permite buscar (cargar en la tabla) por tipo de apartamento y provincia.
La version propuesta por el profesor tiene el boton en la herramienta de tareas y recibe los parametros de busqueda de las cajas tipo y municipio de la ventana (las que se utilizan para crear).*🪛
- ✅Para dar de baja el inmueble no puede estar disponible
- ✅Si se modifica la fecha de baja y se vacia (vuelve a estar de alta) el inmueble tiene que pasar a esatr disponible
- El boton de limpiar recarga la tabla sin filtros
- ✅El valor por defecto de un inmueble debe ser disponible
- ✅El tema de que puedas marcar el tipo de operacion como alquiler y poner solo el precio de venta.....

*Propuesta: Apartado de filtros de busqueda con el historico y estas movidas. Si ocupa mucho espacio que se haga desplegable. A la hora de cargar hacer varias funciones que busquen segun numero de parametrops??? polimorfismo en python??
    https://www.geeksforgeeks.org/python-method-overloading/

##07/11/2024

- Al dar de alta una propiedad o cliente el campo de fecha baja debe de estar vacio // No de acuerdo con esto.
- al dar de baja o alta las fechas tienen que tener sentido
- En la tabla de propiedades precio venta y alquiler aparecen en el orden inverso
- Cambia las comprobaciones de las cargas para que no vayan segun indice, si no por tipo de qt ( si es una combobox que es con current text que la localice por ser del tipo combo box y no por ser el indice 14)
- Ponle color a la tab seleccionada

## 13/11/24
- Comprueba que las fechas tengan formato valido, que el cliente no meta texto
- opcion exportar datos, exportar datos clientes json o csv. En herramientas>exportar datos> exportar clientes JSON, exportar clientes CSV*
- Añadir atajos de teclado a las opciones de exportar backup y estas cosas. ctr+B (crear backup)

*Para hacer exports a json y csv hay que instalar unas librerias, esta en los apuntes
````python
 def exportCSVProp(self):
        try:
            fecha = datetime.today()
            fecha = fecha.strftime('%Y_%m_%d_%H_%M_%S')
            file = (str(fecha) + '_DatosPropiedades.csv')
            directorio, fichero = var.dlgabrir.getSaveFileName(None, "Exporta Datos en CSV", file, ".csv")
            if fichero:
                registros = conexion.Conexion.listadoPropiedades(self)
                with open(fichero, 'w', newline='', encondig='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(["Codigo", "Alta", "Baja", "Dirección", "Provincia", "Municipio", "Tipo", "NºHabitaciones", "NºBaños", "Superficie", "Precio Alquiler", "Precio Compra", 
                                     "Código Postal", "Observaciones", "Operación", "Estado", "Propietario", "Móvil"])
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
````