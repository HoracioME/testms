from operator import ne
from typing import Any
from sqlalchemy.sql.expression import except_

from sqlalchemy.sql.sqltypes import Date
from starlette import status
from db.errores_uow import (
    SqlAlchemyUnitOfWork,
    RegistroErrorUnitOfWork)

from datetime import date, datetime

import requests
from model.errors import EntityNotFoundException

from model.rest import TestData, TestResponse, CatalogoErroresData
from fastapi import HTTPException

from model.domain.error_model import LogErrorModel
from model.domain.info_error_model import InfoErrorModel
from loguru import logger

HTTP_SESSION = requests.Session()























def agregar_error(modulo: int, tipo_cuenta: int, codigo: str, excep: str) -> int:
    """es mecesario encapsular el unit of work en un try catch para capturar los errores"""
    try:
        with RegistroErrorUnitOfWork() as uow:
            id_mod = uow.modulo_repository.get(modulo)
            if not id_mod:
                logger.error("El modulo {} no existe".format(modulo))
                raise EntityNotFoundException(
                    description="El modulo {} no existe".format(modulo))
            error_descripcion = uow.info_error_repository.get_by_code(codigo)
            if not error_descripcion:
                logger.error(
                    "el codigo {} mp se emcuentra registrado en la db".format(codigo)
                )
            tipo_cuenta = uow.tipo_cuenta_repository.get(tipo_cuenta)
            if not tipo_cuenta:
                logger.error("la cuenta no existe")
                raise EntityNotFoundException(
                    descripcion="la cuenta no existe"
                )
            nuevo_registro = LogErrorModel(
                tipo_cuenta=tipo_cuenta.Id,
                info_error=error_descripcion.IdError,
                fecha = datetime.now(),
                excep=excep
            )
            uow.error_repository.add(nuevo_registro)
            uow.commit()
            return nuevo_registro.LogErrorId
    except EntityNotFoundException as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as exc:
        logger.exception(exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
            headers={"WWW-Authenticate": "Bearer"},
        )
        
def obtener_catalogo_errores(modulo_id:int) -> Any:
    try:
        with RegistroErrorUnitOfWork() as uow:
            modulo = uow.modulo_repository.get(modulo_id)
            if not modulo:
                logger.error("El modulo {} no existe".format(modulo))
                raise EntityNotFoundException(descripcion = "El modulo {} no existe".format(modulo))
            #buscar errores
            errors_detail = uow.info_error_repository.obtener_catalogo_errores(modulo_id)
            cat_errors=[]
            #import pdb; pdb.set_trace()
            for e in errors_detail:
                cat_errors.append(
                    CatalogoErroresData(
                        codigoError = e.CodigoError,
                        descripcion = e.Descripcion,
                        url_servicio = e.UrlServicio)
                )
            return cat_errors

    except EntityNotFoundException as e:
        raise HTTPException(
            status_code = status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail = str(e),
            headers = {"WWW-Authenticate":"Bearer"}
            )
    except Exception as e:
        logger.exception(e)
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = str(e),
            headers = {"WWW-Authenticate":"Bearer"}
            )
        
def actualiza_error(codigo_error:str, nueva_descripcion:str, nueva_url:str) -> Any:
    try:
        with RegistroErrorUnitOfWork() as uow:
            error_a_modificar = uow.info_error_repository.get_by_code(codigo_error)
            if not error_a_modificar:
                logger.error("El error a modificar no existe")
                raise EntityNotFoundException(descripcion = "El error a modificar no existe")
            
            error_a_modificar.UrlServicio = nueva_url
            error_a_modificar.Descripcion = nueva_descripcion
            uow.info_error_repository.add(error_a_modificar)
            uow.commit()
            return 1
    
    except EntityNotFoundException as e:
        raise HTTPException(
            status_code = status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail = str(e),
            headers = {"WWW-Authenticate":"Bearer"}
        )
    except Exception as e:
        logger.exception(e)
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = str(e),
            headers = {"WWW-Authenticate":"Bearer"}
        )