import yaml  # YAML parsing
import sys  # Parsing arguments of the script
import os
import time
from jinja2 import Environment, FileSystemLoader, Template  # Jinja template


def my_finalize(thing):
    # This avoids filling in with 'None' if a field is undefined
    return thing if thing is not None else ''


# Folder with data and templates and do extension
ENV = Environment(loader=FileSystemLoader('.'), extensions=[
                  'jinja2.ext.do'], finalize=my_finalize)

# Loading the template file
plantilla = ENV.get_template("template/cservicio.j2")


def yaml_loader(filepath):
    # Loads a yaml file
    with open(filepath, 'r') as file_descriptor:
        data = yaml.load(file_descriptor, Loader=yaml.FullLoader)
    return data


# read data file path
datos = sys.argv[1]
# output folder name
carpeta = os.path.splitext(os.path.basename(datos))[0]+"_cservicio"
# create output folder
if not os.path.exists(carpeta):
    os.makedirs(carpeta)

# read config data file
config = yaml_loader("data/config.yaml")
# read current job data
thiscs = yaml_loader(datos)
# Merge the dictionaries with preference for the current job data
config.update(thiscs)


def funcion():
    # Opening the output file
    with open(carpeta+"/cservicio.tex", 'w', encoding="utf8") as file:
        # Rendering the output from data and template
        salida = plantilla.render(config)
        file.write(salida)  # Creating the output file
        file.close  # Closing the output file
    # Compile output file
    os.system("pdflatex -output-directory=" +
              carpeta+" "+carpeta+"/cservicio.tex")
