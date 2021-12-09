from datetime import date
from sqlalchemy.sql.sqltypes import Date

class LogErrorModel:
    def __init__(self, tipo_cuenta:int, info_error:int, fecha:Date, excep:str):
        self.LogErrorId: int
        self.IdTipoCuenta = tipo_cuenta
        self.Id: int
        self.IdInfoError = info_error
        self.Fecha = fecha
        self.ErrorExep = excep
        
    def __str__(self) -> str:
        return "error id: {}".format(self.LogErrorId)
        