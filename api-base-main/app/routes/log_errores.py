from fastapi import APIRouter, Body, Depends, HTTPException
from model.errors import EntityNotFoundException
from services import errores_handler as handler
from fastapi_jwt_auth import AuthJWT
from common.api.responses import responses as HTTP_RESPONSES

from model.rest import CatalogoErroresData, ResponseActualizaCatErrores, ResponseCatalogoErrores, TestData,TestRequest,TestResponse,DatosAlta,ErrorData,ResponseLogError, UpdateDataCatErrores


##########################################################################
### Se pueden definir errores personalizados (ver la implementación en el
### archivo EntityNotFoundException)
##########################################################################
router = APIRouter(responses=HTTP_RESPONSES)

##########################################################################
### Se definen los parámetros que se reciben y los que se devuelven con base
### en el modelo
##########################################################################


@router.post("/agregar-error", response_model = ResponseLogError)
async def agregar_nuevo_registro_error(data:ErrorData)-> ResponseLogError:
    error_id = handler.agregar_error(data.id_modulo, data.id_tipo_cuenta,
                                    data.codigo_error, data.error_excep)
    return ResponseLogError(
        estatus = 1,
        mensaje = "operación exitosa",
        error_id = error_id
    )
    
@router.get("/{id_modulo}/obtener-catalogo", response_model = ResponseCatalogoErrores)
async def obtener_catalogo(id_modulo:int) -> ResponseCatalogoErrores:
    try:
        registros = handler.obtener_catalogo_errores(id_modulo)
        
        if(not registros):
            raise EntityNotFoundException(descripcion="No hay elementos")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return ResponseCatalogoErrores(
        estatus = 1,
        mensaje = "OK",
        catalogo = registros
    )
    
@router.put("/{codigo_error}/actualiza-cat-errores", response_model = ResponseActualizaCatErrores)
async def actualiza_cat_errores(data:UpdateDataCatErrores) -> ResponseActualizaCatErrores:
    
    registro = handler.actualiza_error(data.codigo_error, data.nueva_descripcion, data.nueva_url)
    
    return ResponseActualizaCatErrores(
        estatus = 1,
        mensaje = "OK",
        registro = registro
    )
    
@router.get("/get", response_model=TestResponse)
async def test(id:int = 0, authorize:AuthJWT = Depends()) -> TestResponse:
    # descomentar la siguiente linea si se tiene implementado el ART de autentificación
    try:
        registro = handler.obtener_registro(id)
        
        if(not registro):
            raise EntityNotFoundException(description="El registro")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    return TestResponse(
        estatus = 1,
        mensaje = "OK",
        datos=TestData(
            valor1 = registro.Id,
            valor2 = registro.Mensaje
        )
    )