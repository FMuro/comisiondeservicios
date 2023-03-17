# Comisión de servicios de la Universidad de Sevilla

Es un script de python, ejecutable desde la línea de comandos, que produce una solicitud de comisión de servicios de la Universidad de Sevilla en PDF a partir de los datos básicos. La plantilla actual está basada en el modelo oficial del 27-1-2021.

Si lo prefieres, puedes simplemente descargar el fichero [`test.tex`](test/test.tex), modificarlo con tus datos y compilarlo sin instalar el script.

# Instalación

TO-DO.
# Instrucciones de uso

Necesitas crear un fichero de texto plano con los datos de la comisión de servicio. Puedes descargar el modelo [`test.yaml`](test/test.yaml), cambiarlo de nombre y editarlo con tus datos.

Para generar la solicitud de comisión de servicio en PDF tienes que ejecutar el script del siguiente modo:

`cservicio test.yaml`

Esto generará un PDF con el mismo nombre en el directorio de ejecución, en este caso `test.pdf`.

Si el resultado no fuera el deseado, puedes obtener el archivo TeX en lugar de un PDF ejecutando:

`cservicio -tex test.yaml`

Esto generará un archivo TeX con el mismo nombre en el directorio de ejecución, en este caso `test.tex`. Puedes editar este archivo para intentar obtener un mejor resultado. 

Si quieres compilar el TeX en un ordenador donde este script no esté instalado, tendrás que copiar el logotipo. La ruta aparece dentro del fichero TeX.

![](img/cs.png)
