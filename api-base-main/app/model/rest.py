from pydantic import BaseModel
from typing import Optional

################################################################################
### Clases(json) que se reciben
################################################################################

class TestRequest(BaseModel):
    primer_campo: str
    segundo_campo: str
    tercer_campo: Optional[str] = None

class DatosAlta(BaseModel):
    nombre:str
    comentarios:str
    
### Registrar error
class ErrorAlta(BaseModel):
    pass

class ErrorData(BaseModel):
    id_modulo:int
    id_tipo_cuenta:int
    codigo_error:str
    error_excep:str
    
class UpdateDataCatErrores(BaseModel):
    codigo_error:str
    nueva_descripcion:str
    nueva_url:str

################################################################################
### Clases que se envían
################################################################################

class TestData(BaseModel):
    valor1: int
    valor2: str

class TestResponse(BaseModel):
    estatus: int
    mensaje: str
    datos: TestData

class ResponseLogError(BaseModel):
    estatus: int
    mensaje: str
    error_id: int

class CatalogoErroresData(BaseModel):
    codigoError: str
    descripcion: str
    url_servicio: Optional[str]
    
class ResponseCatalogoErrores(BaseModel):
    estatus: int
    mensaje: str
    catalogo: list[CatalogoErroresData]
    
class ResponseActualizaCatErrores(BaseModel):
    estatus: int
    mensaje: str