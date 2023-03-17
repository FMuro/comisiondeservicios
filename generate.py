import yaml  # YAML parsing

import sys  # Parsing arguments of the script

from jinja2 import Environment, FileSystemLoader, Template  # Jinja template


def my_finalize(thing):  # This avoids filling in with 'None' if a field is undefined
    return thing if thing is not None else ''


# Folder with data and templates and do extension
ENV = Environment(loader=FileSystemLoader('.'), extensions=[
                  'jinja2.ext.do'], finalize=my_finalize)

plantilla = ENV.get_template("template/cs.j2")  # Loading the template file

with open(sys.argv[1]) as y:  # Opening the data file
    entrada = yaml.load(y, Loader=yaml.FullLoader)  # Loading the YAML data
    f = open(sys.argv[2], 'w', encoding="utf8")  # Opening the output file
    # Rendering the output from data and template
    salida = plantilla.render(entrada)
    f.write(salida)  # Creating the output file
    f.close  # Closing the output file
