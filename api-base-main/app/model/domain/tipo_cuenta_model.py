""" clase que mapea la tabla cat_tipo,
    catalogo tipo cuenta
"""
from datetime import date

from sqlalchemy.sql.sqltypes import Date

class TipoCuentaModel:
    def __init__(self):
        self.Id: int
        self.TipoCuenta: str
        
"""reglas de negocio"""