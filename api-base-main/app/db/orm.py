from sqlalchemy import (
    Table,
    MetaData,
    Column,
    Integer,
    String,
    Date,
    Text,
)
from sqlalchemy.orm import mapper, relationship
from sqlalchemy.sql.expression import false
from sqlalchemy.sql.operators import collate
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import DateTime, SmallInteger
from model.domain.base_model import BaseModel
from model.domain.modulo_model import ModuloModel
from model.domain.tipo_cuenta_model import TipoCuentaModel
from model.domain.info_error_model import InfoErrorModel
from model.domain.error_model import LogErrorModel

metadata = MetaData()
################################################################################
### Se debe de realizar el mapeo entre clases de negocio y la base de datos
### el mapeo se hace del modo "tradicional" de SQLAlquemy
################################################################################
cat_modulo = Table (
    "cat_modulo",
    metadata,
    Column("id_modulo", SmallInteger, primary_key=True, autoincrement=True),
    Column("modulo", String(20), nullable=False, unique=True),
)

cat_tipo = Table (
    "cat_tipo",
    metadata,
    Column("id_tipo", SmallInteger, primary_key=True, autoincrement=True),
    Column("tipo", String(15), nullable=False, unique=True),
)

cat_errores = Table (
    "cat_errores",
    metadata,
    Column("id_error", SmallInteger, primary_key=True, autoincrement=True),
    Column("codigo_error", String(6), nullable=False),
    Column("url_servicio", String(50), nullable=True),
    Column("descripcion", Text, nullable=True),
    Column("id_modulo", SmallInteger, ForeignKey('cat_modulo.id_modulo')),
)

tbl_log_errores = Table (
    "tbl_log_errores",
    metadata,
    Column("id_log_error", Integer, primary_key=True, autoincrement=True),
    Column("id_tipo", SmallInteger, ForeignKey('cat_tipo.id_tipo')),
    Column("id", Integer, nullable=False),
    Column("id_error", SmallInteger, ForeignKey('cat_errores.id_error')),
    Column("fecha", DateTime, nullable=False),
    Column("error_e", Text, nullable=True)
)

################################################################################
### Este método se llama al inicio del programa, no se debe de cambiar el
### nombre de la función y debe de contener todos los mapeos
################################################################################
def start_mappers():
    mapper(ModuloModel, cat_modulo, properties={
        'Id':cat_modulo.c.id_modulo,
        'NombreMod':cat_modulo.c.modulo,
    },
    )
    
    mapper(TipoCuentaModel, cat_tipo, properties={
        'Id':cat_tipo.c.id_tipo,
        'TipoCuenta':cat_tipo.c.tipo,
        #'logErrores':relationship(InfoError,backref='cat_tipo',order_by=tbl_log_errores.c.id_log_error)
    },
    )
    
    mapper(InfoErrorModel, cat_errores, properties={
        'IdError':cat_errores.c.id_error,
        'CodigoError':cat_errores.c.codigo_error,
        'Descripcion':cat_errores.c.descripcion,
        'ModuloId':cat_errores.c.id_modulo,
        'UrlServicio':cat_errores.c.url_servicio,
    },
    )
    
    mapper(LogErrorModel,tbl_log_errores,properties={
        'LogErrorId':tbl_log_errores.c.id_log_error,
        'IdTipoCuenta':tbl_log_errores.c.id_tipo,
        'Id':tbl_log_errores.c.id,
        'IdInfoError':tbl_log_errores.c.id_error,
        'Fecha':tbl_log_errores.c.fecha,
        'ErrorExep':tbl_log_errores.c.error_e,
    },
    )
