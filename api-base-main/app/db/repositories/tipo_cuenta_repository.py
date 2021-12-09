from operator import imod
from typing import Any
from sqlalchemy.sql.expression import false, true
from sqlalchemy.sql import select, and_

from common.db.base import BaseRepository
from model.domain.tipo_cuenta_model import TipoCuentaModel

class TipoCuentaRepository(BaseRepository):
    def __init__(self, session) -> None:
        super().__init__()
        self.session = session
        
    def get(self, id: int) -> Any:
        return self.session.query(TipoCuentaModel).filter_by(Id=id).first()
    
    def add(self, tipo_cuenta_model:TipoCuentaModel):
        self.session.add(tipo_cuenta_model)