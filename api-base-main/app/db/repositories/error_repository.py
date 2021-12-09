from typing import Any

from common.db.base import BaseRepository
from model.domain.error_model import LogErrorModel
"""el repository es la conexion entre la base de datos y la clase"""

class ErrorRepository(BaseRepository):
    def __init__(self, session) -> None:
        super().__init__()
        self.session = session
        
    def get(self, id: int) -> Any:
        return self.session.query(LogErrorModel).filter_by(Id=id).first()
    
    def add(self, log_error_model):
        self.session.add(log_error_model)
        self.session.flush()
        self.session.refresh(log_error_model)