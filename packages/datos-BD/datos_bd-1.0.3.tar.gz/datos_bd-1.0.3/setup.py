import pathlib
from setuptools import find_packages, setup


HERE = pathlib.Path(__file__).parent

VERSION = '1.0.3'
PACKAGE_NAME = 'datos_BD'
AUTHOR = 'Alan Adalberto Ortiz Pérez'
AUTHOR_EMAIL = 'aortiz@isssteson.gob.mx'
URL = ''

LICENSE = '© ISSSTESON'
DESCRIPTION = 'Librería para acceder a los Datos de conexión a servidores del Instituto de Seguridad y Servicios Sociales de los Trabajadores del Estado de Sonora (ISSSTESON).'''
LONG_DESCRIPTION = (HERE / "README.md").read_text(encoding='utf-8')
LONG_DESC_TYPE = 'text/markdown'

# Paquetes necesarios para el funcionamiento de la Librería
INSTALL_REQUIRES = [

]

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type=LONG_DESC_TYPE,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    #install_requires = INSTALL_REQUIRES,
    license=LICENSE,
    packages=find_packages(),
    include_package_data=True
)