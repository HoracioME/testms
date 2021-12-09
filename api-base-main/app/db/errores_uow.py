from fastapi.applications import FastAPI
from common.db.unit_of_work import AbstractUnitOfWork, DEFAULT_SESSION_FACTORY
from db.repositories.error_repository import ErrorRepository
from db.repositories.info_error_repository import InfoErrorRepository
from db.repositories.modulo_repository import ModuloRepository
from db.repositories.tipo_cuenta_repository import TipoCuentaRepository


class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    def __enter__(self, session_factory = DEFAULT_SESSION_FACTORY):
        self.session = session_factory(expire_on_commit=False)
        self.base_repository = TipoCuentaRepository(self.session)
        self.info_error_repository = InfoErrorRepository(self.session)
        return self

    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close() #(3)
        
    def commit(self): #(4)
        self.session.commit()
        
    def rollback(self): #(4)
        self.session.rollback()
    
"""unit of work que maneja el registro de errores"""

class RegistroErrorUnitOfWork(AbstractUnitOfWork):
    def __enter__(self, session_factory = DEFAULT_SESSION_FACTORY):
        self.session = session_factory(expire_on_commit=False)
        self.error_repository = ErrorRepository(self.session)
        self.info_error_repository = InfoErrorRepository(self.session)
        self.modulo_repository = ModuloRepository(self.session)
        self.tipo_cuenta_repository = TipoCuentaRepository(self.session)
        return self
    
    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close()   #(3)
        
    def commit(self): #(4)
        self.session.commit()
        
    def rollback(self):  #(4)
        self.session.rollback()