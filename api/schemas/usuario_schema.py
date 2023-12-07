from pydantic import BaseModel
from typing import Optional, List
from model.usuario import Usuario
import json
import numpy as np

class UsuarioSchema(BaseModel):
    """ Define como um novo usuário deve ser inserido e ser representado
    """
    name: str = "Maria"
    userid: int = 19706085
    age: int = 35
    estimatedsalary: int = 20000
    gender: int = 0
   
    
class UsuarioViewSchema(BaseModel):
    """Define como um usuário será retornado
    """

    id: int = 1
    name: str = "Maria"
    userid: int = 19706085
    age: int = 35
    estimatedsalary: int = 20000
    gender: int = 0
    purchased: int = None
    
    
class UsuarioBuscaSchema(BaseModel):
    """Define como deve ser a estrutura que representa a busca.
    Ela será feita com base no nome do usuário.
    """
    name: str = "Maria"

class ListaUsuariosSchema(BaseModel):
    """Define como uma lista de usuários será representada
    """
    usuarios: List[UsuarioSchema]

    
class UsuarioDelSchema(BaseModel):
    """Define como um usuário para deleção será representado
    """
    name: str = "Maria"
    
# Apresenta apenas os dados de um usuário    
def apresenta_usuario(usuario: Usuario):
    """ Retorna uma representação do usuário seguindo o schema definido em
        UsuarioViewSchema.
    """
    return {
        "id":usuario.id,
        "name": usuario.name,
        "userid": usuario.userid,
        "age": usuario.age,
        "estimatedsalary": usuario.estimatedsalary,
        "gender": usuario.gender,
        "purchased": usuario.purchased                

    }
    
# Apresenta uma lista de usuários
def apresenta_usuarios(usuarios: List[Usuario]):
    """ Retorna uma representação do usuário seguindo o schema definido em
        UsuarioViewSchema.
    """
    result = []
    for usuario in usuarios:
        result.append({
            "id":usuario.id,
            "name":usuario.name,
            "userid": usuario.userid,
            "age": usuario.age,
            "estimatedsalary": usuario.estimatedsalary,
            "gender": usuario.gender,
            "purchased": usuario.purchased
        })

    return {"usuarios": result}

