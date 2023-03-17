# Comisión de servicios de la Universidad de Sevilla

Es un script de python, ejecutable desde la línea de comandos, que produce una solicitud de comisión de servicios de la Universidad de Sevilla en PDF a partir de los datos básicos. La plantilla actual está basada en el modelo oficial del 27-1-2021.

Si lo prefieres, puedes simplemente copiar [`test.tex`](tests/test.tex), descargar [`logo.pdf`](csus/logo.pdf), modificar el firecho TeX con tus datos y la ruta correcta al logotipo y compilarlo sin instalar el script.

# Instalación

Ejecuta el siguiente comando en tu terminal:

```
pip install --upgrade git+https://github.com/FMuro/comisiondeservicios.git#egg=csus
```

# Instrucciones de uso

Necesitas crear un fichero de texto plano con los datos de la comisión de servicio. Puedes copiar el modelo [`test.yaml`](tests/test.yaml), cambiarlo de nombre y editarlo con tus datos.

Para generar la solicitud de comisión de servicio en PDF tienes que ejecutar el script del siguiente modo:

```
cservicio test.yaml
```

Esto generará un PDF con el mismo nombre en el directorio de ejecución, en este caso `test.pdf`.

Si el resultado no fuera el deseado, puedes obtener el archivo TeX en lugar de un PDF ejecutando:

```
cservicio -tex test.yaml
```

Esto generará un archivo TeX con el mismo nombre en el directorio de ejecución, en este caso `test.tex`. Puedes editar este archivo para intentar obtener un mejor resultado. 

Si quieres compilar el TeX en un ordenador donde este script no esté instalado, tendrás que copiar el logotipo. La ruta aparece dentro del fichero TeX.

# Desinstalación

```
pip uninstall csus
```

![](img/test.png)
