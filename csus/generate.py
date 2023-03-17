import yaml  # YAML parsing
import sys  # Parsing arguments of the script
import os  # interact with the operating system
import shutil  # copy files
import tempfile  # temporary folders and files
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


def funcion():
    # read data file path
    datos = args[0]
    # file name
    nombre = os.path.splitext(os.path.basename(datos))[0]
    # add script path to make template and logo available
    config = {"camino": str(script_path)}
    with open(datos, 'r') as file_descriptor:
        # get job data
        config.update(yaml.load(file_descriptor, Loader=yaml.BaseLoader))
    with tempfile.TemporaryDirectory() as carpeta:
        # Opening the output file
        with open(carpeta+"/"+nombre+".tex", 'w', encoding="utf8") as file:
            # Loading the template file
            plantilla = ENV.get_template("/cservicio.j2")
            # Rendering the output from data and template
            salida = plantilla.render(config)
            file.write(salida)  # Creating the output file
            file.close  # Closing the output file
        # Compile output file
        if "-tex" in opts:
            shutil.copy(carpeta+"/"+nombre+".tex", ".")
        else:
            os.system("pdflatex -output-directory=" +
                      carpeta+" "+carpeta+"/"+nombre+".tex")
            shutil.copy(carpeta+"/"+nombre+".pdf", ".")
