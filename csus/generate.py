import yaml  # YAML parsing
import sys  # Parsing arguments of the script
import os  # interact with the operating system
import shutil  # copy files
import tempfile  # temporary folders and files
from datetime import datetime  # deal with dates
from dateutil.relativedelta import relativedelta  # date computations
from jinja2 import Environment, FileSystemLoader, Template  # Jinja template

# separate user-provided options and arguments
# only expected yaml file as argument
opts = [opt for opt in sys.argv[1:] if opt.startswith("-")]
args = [arg for arg in sys.argv[1:] if not arg.startswith("-")]

# script path
script_path = os.path.dirname(os.path.realpath(__file__))
print(script_path)


def my_finalize(thing):
    # This avoids filling in with 'None' if a field is undefined
    return thing if thing is not None else ''


# Folder with data and templates and do extension
ENV = Environment(loader=FileSystemLoader(script_path), extensions=[
                  'jinja2.ext.do'], finalize=my_finalize)


def datetime_format(value, format="%d-%m-%Y"):
    return value.strftime(format)


ENV.filters["datetime_format"] = datetime_format


def funcion():
    # read data file path
    datos = args[0]
    # file name
    nombre = os.path.splitext(os.path.basename(datos))[0]
    # add script path to make template and logo available
    config = {"camino": str(script_path)}
    with open(datos, 'r') as archivo:
        estretrabajo = yaml.load(archivo, Loader=yaml.BaseLoader)
        # get job data
        if estretrabajo is not None:
            config.update(estretrabajo)
    # get date/time as such in python
    for key in ['ida', 'vuelta']:
        print(config[key])
        config[key] = datetime.strptime(config[key], "%d-%m-%Y %H:%M")
    three_months_from_ida = config['ida'] + relativedelta(months=+3)
    fifteen_days_from_ida = config['ida'] + relativedelta(days=+15)
    documentos = ['cservicio']
    if config['vuelta'] < fifteen_days_from_ida:
        config.update({"menosde15dias": "menosde15dias"})
        documentos.append('licencia')
    elif config['vuelta'] < three_months_from_ida:
        documentos.append('licencia')
    else:
        config.update({"licencia": "masde3meses"})
    with tempfile.TemporaryDirectory() as carpeta:
        for output in documentos:
            # Opening the output file
            with open(carpeta+"/"+nombre+"_"+output+".tex", 'w', encoding="utf8") as file:
                # Loading the template file
                plantilla = ENV.get_template("/"+output+".j2")
                # Rendering the output from data and template
                salida = plantilla.render(config)
                file.write(salida)  # Creating the output file
                file.close  # Closing the output file
            # Compile output file
            if "-tex" in opts:
                shutil.copy(carpeta+"/"+nombre+"_"+output+".tex", ".")
            else:
                os.system("pdflatex -output-directory=" +
                          carpeta+" "+carpeta+"/"+nombre+"_"+output+".tex")
                shutil.copy(carpeta+"/"+nombre+"_"+output+".pdf", ".")
