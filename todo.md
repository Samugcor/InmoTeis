## 05/11/2024

- Añadir propiedades. ✅
- Eliminar propiedades.
- Modificar propiedades.✅

- Cargar propiedades en la tabla, campos: codigo, municipio, tipo propiedad habitaciones baño precio alquiler, precio venta tipo operacion. Los precios deben añadir el simbolo del euro (hardcode) y si estan vacios "- €".
Añade una columna para la baja de la propiedad.✅

- Haz que funcione el historico.✅
- Haz que el boton de borrar borre también el formulario de propiedades. (Estaria bien que borre dependiendo de la pestaña en la que estás).
- Nueva funcion de la barra de herramientas "lupa"

- Validar telefono propiedad
- Validar codigo postal

## 06/11/2024

- La nueva funcion "lupa" (buscar) permite buscar (cargar en la tabla) por tipo de apartamento y provincia.
La version propuesta por el profesor tiene el boton en la herramienta de tareas y recibe los parametros de busqueda de las cajas tipo y municipio de la ventana (las que se utilizan para crear).*
- Para dar de baja el inmueble no puede estar disponible
- Si se modifica la fecha de baja y se vacia (vuelve a estar de alta) el inmueble tiene que pasar a esatr disponible
- El boton de limpiar recarga la tabla sin filtros
- El valor por defecto de un inmueble deb ser disponible
- El tema de que puedas marcar el tipo de operacion como alquiler y poner solo el precio de venta.....

*Propuesta: Apartado de filtros de busqueda con el historico y estas movidas. Si ocupa mucho espacio que se haga desplegable. A la hora de cargar hacer varias funciones que busquen segun numero de parametrops??? polimorfismo en python??
    https://www.geeksforgeeks.org/python-method-overloading/

##07/11/2024

- Al dar de alta una propiedad o cliente el campo de fecha baja debe de estar vacio
- al dar de baja o alta las fechas tienen que tener sentido
- En la tabla de propiedades precio venta y alquiler aparecen en el orden inverso