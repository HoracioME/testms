""" clase que mapea la tabla cat_modulo
    catalogo modulos del sistema de vexi
"""
from datetime import date

from sqlalchemy.sql.sqltypes import Date

class ModuloModel:
    def __init__(self):
        self.Id: int
        self.NombreMod
        