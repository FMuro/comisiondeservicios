import yaml  # YAML parsing
import argparse  # Parsing arguments of the script
import os  # interact with the operating system
import shutil  # copy files
import tempfile  # temporary folders and files
from datetime import datetime  # deal with dates
from dateutil.relativedelta import relativedelta  # date computations
from jinja2 import Environment, FileSystemLoader  # Jinja template
import platform  # check OS
import subprocess  # open file with default program
from appdirs import *

# CLI arguments

parser = argparse.ArgumentParser(
    prog='cservicios',
    description='Rellena la documentación necesaria para una comisión de servicios de la Universidad de Sevilla',
    epilog='¡Disfruta de tus tareas administrativas!')

parser.add_argument(
    '-f', '--file', help="archivo YAML con los datos de tu comisión de servicio")
parser.add_argument(
    '-i', '--initialize', nargs='?', type=str, const='csdatos.yaml',
    help="crea un archivo YAML con el nombre indicado y el contenido por defecto")
parser.add_argument('-t', '--tex', action='store_true',
                    help='genera los archivos TeX')
parser.add_argument('-c', '--config', action='store_true',
                    help='edita el archivo YAML que se usará por defecto')

args = parser.parse_args()

# script path
script_path = os.path.dirname(os.path.realpath(__file__))


def open_text_file(datos):
    OS = platform.platform()
    if "macOS" in OS:
        subprocess.Popen(('open', datos))
    elif "Windows" in OS:
        subprocess.Popen(('notepad.exe', datos))
    else:
        subprocess.Popen(('xdg-open', datos))


def my_finalize(thing):
    # This avoids filling in with 'None' if a field is undefined
    return thing if thing is not None else ''


# Folder with data and templates and do extension
ENV = Environment(loader=FileSystemLoader(script_path), extensions=[
                  'jinja2.ext.do'], finalize=my_finalize)


def datetime_format(value, format="%d-%m-%Y"):
    return value.strftime(format)


ENV.filters["datetime_format"] = datetime_format

config_folder = user_config_dir('csus', 'fmuro')
config_file = os.path.join(config_folder, "csdatos.yaml")


def funcion():
    if not os.path.exists(config_file):
        os.makedirs(config_folder, exist_ok=True)
        shutil.copy(os.path.join(
            script_path, "csdatos.yaml"), config_folder)
    if args.config:
        print("Edita el archivo 'csdatos.yaml' con tus datos personales y habituales para futuros usos")
        open_text_file(config_file)
    elif args.initialize:
        # read data file path
        datos = args.initialize
        # file name
        nombre = os.path.splitext(os.path.basename(datos))[0]
        if not os.path.exists("./"+nombre+".yaml"):
            shutil.copy(config_file, "./"+nombre+".yaml")
        print("Edita el archivo '" + nombre +
              ".yaml' y ejecuta 'cservicios -f " + nombre + ".yaml'")
        open_text_file(nombre+".yaml")
    elif args.file is not None:
        # read data file path
        datos = args.file
        # file name
        nombre = os.path.splitext(os.path.basename(datos))[0]
        # add script path to make template and logo available
        config = {"camino": str(script_path)}
        with open(datos, 'r') as archivo:
            estetrabajo = yaml.load(archivo, Loader=yaml.BaseLoader)
            # get job data
            if estetrabajo is not None:
                config.update(estetrabajo)
        # get date/time as such in python
        for key in ['ida', 'vuelta']:
            config[key] = datetime.strptime(config[key], "%d-%m-%Y %H:%M")
        three_months_from_ida = config['ida'] + relativedelta(months=+3)
        fifteen_days_from_ida = config['ida'] + relativedelta(days=+15)
        documentos = ['cservicios']
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
                with open(os.path.join(carpeta, nombre+"_"+output+".tex"), 'w', encoding="utf8") as file:
                    # Loading the template file
                    plantilla = ENV.get_template("/"+output+".j2")
                    # Rendering the output from data and template
                    salida = plantilla.render(config)
                    file.write(salida)  # Creating the output file
                    file.close  # Closing the output file
                # Compile output file
                if args.tex:
                    shutil.copy(os.path.join(
                        carpeta, nombre+"_"+output+".tex"), ".")
                else:
                    os.system("pdflatex -output-directory=" +
                              carpeta+" "+os.path.join(carpeta, nombre+"_"+output+".tex"))
                    shutil.copy(os.path.join(
                        carpeta, nombre+"_"+output+".pdf"), ".")
    else:
        print("Run 'cservicios -h' for help")
