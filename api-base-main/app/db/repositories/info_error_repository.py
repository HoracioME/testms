from typing import Any
from sqlalchemy.sql.expression import false, true
from sqlalchemy.sql import select, and_

from common.db.base import BaseRepository
from model.domain.info_error_model import InfoErrorModel

class InfoErrorRepository(BaseRepository):
    def __init__(self, session) -> None:
        super().__init__()
        self.session = session
    
    def get(self, id: int) -> Any:
        return self.session.query(InfoErrorModel).filter_by(Id=id).first()
    
    def add(self, info_error_model:InfoErrorModel):
        self.session.add(info_error_model)
        
    def get_by_code(self, code:str) -> Any:
        return self.session.query(InfoErrorModel).filter_by(CodigoError=code).first()
    
    def obtener_catalogo_errores(self, id_modulo:int) -> Any:
        return self.session.query(InfoErrorModel).filter_by(ModuloId = id_modulo).all()