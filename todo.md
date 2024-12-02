## 05/11/2024

- ✅Añadir propiedades. 
- ✅Eliminar propiedades.
- ✅Modificar propiedades.

- ✅Cargar propiedades en la tabla, campos: codigo, municipio, tipo propiedad habitaciones baño precio alquiler, precio venta tipo operacion. Los precios deben añadir el simbolo del euro (hardcode) y si estan vacios "- €".
Añade una columna para la baja de la propiedad.

- ✅Haz que funcione el historico.
- ✅Haz que el boton de borrar borre también el formulario de propiedades. (Estaria bien que borre dependiendo de la pestaña en la que estás).

~~- Nueva funcion de la barra de herramientas "lupa"~~

- Validar telefono propiedad
- Validar codigo postal

## 06/11/2024

- ✅La nueva funcion "lupa" (buscar) permite buscar (cargar en la tabla) por tipo de apartamento y provincia.
La version propuesta por el profesor tiene el boton en la herramienta de tareas y recibe los parametros de busqueda de las cajas tipo y municipio de la ventana (las que se utilizan para crear).*
- ✅Para dar de baja el inmueble no puede estar disponible
- ✅Si se modifica la fecha de baja y se vacia (vuelve a estar de alta) el inmueble tiene que pasar a esatr disponible
- ✅El boton de limpiar recarga la tabla sin filtros
- ✅El valor por defecto de un inmueble debe ser disponible
- ✅El tema de que puedas marcar el tipo de operacion como alquiler y poner solo el precio de venta.....



## 07/11/2024

- Al dar de alta una propiedad o cliente el campo de fecha baja debe de estar vacio // No de acuerdo con esto.
- al dar de baja o alta las fechas tienen que tener sentido
- ✅En la tabla de propiedades precio venta y alquiler aparecen en el orden inverso

~~- Cambia las comprobaciones de las cargas para que no vayan segun indice, si no por tipo de qt ( si es una combobox que es con current text que la localice por ser del tipo combo box y no por ser el indice 14)~~
- ✅Ponle color a la tab seleccionada

## 13/11/24
- Comprueba que las fechas tengan formato valido, que el cliente no meta texto
- ✅ opcion exportar datos, exportar datos clientes json o csv. En herramientas>exportar datos> exportar clientes JSON, exportar clientes CSV*
- Añadir atajos de teclado a las opciones de exportar backup y estas cosas. ctr+B (crear backup)

*Para hacer exports a json y csv hay que instalar unas librerias, esta en los apuntes


## 18/11/2024
- ✅Crea un dialog de acerca de con icono nombre programa, autor y version simbolo compirright ( y un boton para cerrar)
- Cuando das de baja un apropiedad que puede estar vendida alquilada que pregunte por cual en vez de marcar por defecto vendido.
- Muestra un mensaje (metelo en un registro en una columna) de que no hay registros si no muestra nada

## 20/11/2024
- ✅En la pestaña de clientes añade un boton de lupa al lado del dni, cuando el usuario introduce un dni y le da a buscar cargará todos los datos del cliente en la oarte de arriba. Si el cliente no existe te sale un dialog de que no existe.

## 25/11/2024
- Estamos haciendo que ta,bien funcione (solo la parte de clientes ) con la bd del servidor del profesor.
- Cambia el color del registro seleccionado en la tabla por algo más llamativo

## 27/11/2024
- Si te apetece y te sobra el tiempo carga la tabla con paginaciones :) que muestre de 15 en 15 registros o asi

## 02/12/2024
- Cuando limpias que se deseleccione el registro de la tabla (si había uno seleccionado)