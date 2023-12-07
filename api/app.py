from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session, Usuario, Model
from logger import logger
from schemas import *
from flask_cors import CORS

   
# Instanciando o objeto OpenAPI
info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)


# Definindo tags para agrupamento das rotas
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
usuario_tag = Tag(name="Usuario", description="Adição, visualização, remoção e predição de usuários que compraram ou não o produto.")


# Rota home
@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


# Rota de listagem de pacientes
@app.get('/usuarios', tags=[usuario_tag],
         responses={"200": UsuarioViewSchema, "404": ErrorSchema})
def get_usuarios():
    """Lista todos os usuários cadastrados na base
    Retorna uma lista de usuários cadastrados na base.
    
    Args:
        nome (str): nome do usuario
        
    Returns:
        list: lista de usuarios cadastrados na base
    """
    session = Session()
    
    # Buscando todos os usuarios
    usuarios = session.query(Usuario).all()
    
    if not usuarios:
        logger.warning("Não há usuários cadastrados na base :/")
        return {"message": "Não há usuários cadastrados na base :/"}, 404
    else:
        logger.debug(f"%d usuários econtrados" % len(usuarios))
        return apresenta_usuarios(usuarios), 200


# Rota de adição de usuário
@app.post('/usuario', tags=[usuario_tag],
          responses={"200": UsuarioViewSchema, "400": ErrorSchema, "409": ErrorSchema})
def predict(form: UsuarioSchema):
    """Adiciona um novo usuario à base de dados
    Retorna uma representação dos usuários compradores ou não.
    
    Args:
        User ID (int): ID do usuário
        Age (int): idade do usuário
        EstimatedSalary (int): salário estimado do usuário
        Purchased (int): se o usuário comprou ou não o produto
        Gender_encoded (int): gênero do usuário: 1 - Masculino, 0 - Feminino
       
        
    Returns:
        dict: representação do usuário se comprou ou não o produto
    """
    
    # Carregando modelo
    ml_path = 'ml_model/modelo_ads099.pkl'
    modelo = Model.carrega_modelo(ml_path)
    
    usuario = Usuario(
        name=form.name.strip(),
        userid=form.userid,
        age=form.age,
        estimatedsalary=form.estimatedsalary,
        gender=form.gender,
        purchased=Model.preditor(modelo, form)
    )
    logger.debug(f"Adicionando usuário de nome: '{usuario.name}'")
    
    try:
        # Criando conexão com a base
        session = Session()
        
        # Checando se usuario já existe na base
        if session.query(Usuario).filter(Usuario.name == form.name).first():
            error_msg = "Usuário já existente na base :/"
            logger.warning(f"Erro ao adicionar usuario '{usuario.name}', {error_msg}")
            return {"message": error_msg}, 409
        
        # Adicionando usuario
        session.add(usuario)
        # Efetivando o comando de adição
        session.commit()
        # Concluindo a transação
        logger.debug(f"Adicionado usuario de nome: '{usuario.name}'")
        return apresenta_usuario(usuario), 200
    
    # Caso ocorra algum erro na adição
    except Exception as e:
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar usuario '{usuario.name}', {error_msg}")
        return {"message": error_msg}, 400
    

# Métodos baseados em nome
# Rota de busca de usuario por nome
@app.get('/usuario', tags=[usuario_tag],
         responses={"200": UsuarioViewSchema, "404": ErrorSchema})
def get_usuario(query: UsuarioBuscaSchema):    
    """Faz a busca por um usuario cadastrado na base a partir do id

    Args:
        nome (str): nome do ususario
        
    Returns:
        dict: representação do usuário   """
    
    usuario_nome = query.name
    logger.debug(f"Coletando dados sobre o usuário #{usuario_nome}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    usuario = session.query(Usuario).filter(Usuario.name == usuario_nome).first()
    
    if not usuario:
        # se o usuário não foi encontrado
        error_msg = f"Usuario {usuario_nome} não encontrado na base :/"
        logger.warning(f"Erro ao buscar produto '{usuario_nome}', {error_msg}")
        return {"mesage": error_msg}, 404
    else:
        logger.debug(f"Usuário econtrado: '{usuario_nome}'")
        # retorna a representação do usuário
        return apresenta_usuario(usuario), 200
   
    
# Rota de remoção do usuário por nome
@app.delete('/usuario', tags=[usuario_tag],
            responses={"200": UsuarioViewSchema, "404": ErrorSchema})
def delete_usuario(query: UsuarioBuscaSchema):
    """Remove um usuario cadastrado na base a partir do nome

    Args:
        nome (str): nome do usuario
        
    Returns:
        msg: Mensagem de sucesso ou erro
    """
    
    usuario_nome = unquote(query.name)
    logger.debug(f"Deletando dados sobre usuário #{usuario_nome}")
    
    # Criando conexão com a base
    session = Session()
    
    # Buscando usuário
    usuario = session.query(Usuario).filter(Usuario.name == usuario_nome).first()
    
    if not usuario:
        error_msg = "Usuário não encontrado na base :/"
        logger.warning(f"Erro ao deletar paciente '{usuario_nome}', {error_msg}")
        return {"message": error_msg}, 404
    else:
        session.delete(usuario)
        session.commit()
        logger.debug(f"Deletado usuário #{usuario_nome}")
        return {"message": f"Usuário {usuario_nome} removido com sucesso!"}, 200