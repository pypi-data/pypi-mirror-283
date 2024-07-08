
from setuptools import setup

with open("README.rst", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
        name= "prosigue",      # es lo q se ve en "pip list" 
        version= "1.0",
        description= "Realiza una tarea secundaria en cierto tiempo dado. Pero si se cuelga, regresara aun asi al flujo de trabajo principal",
        author= "El Señor es el único eterno. Que la ciencia lo honre a Él.",
        author_email= "",
        long_description=long_description,
        long_description_content_type="text/x-rst",
        license_files=("license.txt",),
        packages= ["prosigue", "prosigue.standard", "prosigue.readme_prosigue"], # ruta: es o son carpetas (es el nomb_paquete para 'from x import y')
        classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
        ],
        python_requires= ">=3.11.3"
)

