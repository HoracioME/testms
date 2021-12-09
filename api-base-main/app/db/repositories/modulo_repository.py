from operator import imod
from typing import Any
from sqlalchemy.sql.expression import false, true
from sqlalchemy.sql import select, and_

from common.db.base import BaseRepository
from model.domain.modulo_model import ModuloModel

class ModuloRepository(BaseRepository):
    def __init__(self, session) -> None:
        super().__init__()
        self.session = session
        
    def get(self, id: int) -> Any:
        return self.session.query(ModuloModel).filter_by(Id=id).first()
    
    def add(self, modulo_model:ModuloModel):
        self.session.add(modulo_model)