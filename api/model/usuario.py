from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from  model import Base


class Usuario(Base):
    __tablename__ = 'usuarios'
    
    id = Column(Integer, primary_key=True)
    name = Column("Name", String(50))
    userid = Column("UserID", Integer)
    age = Column("Age", Integer)
    estimatedsalary = Column("EstimatedSalary", Integer)
    gender = Column("Gender", Integer)
    purchased = Column("Purchased", Integer, nullable=True)
    data_insercao = Column(DateTime, default=datetime.now())
    
    def __init__(self, userid:int, age:int, estimatedsalary:int, name:str,
                 gender:int,  purchased: int,                
                 data_insercao:Union[DateTime, None] = None):
        """
        Cria um Usuário

        Arguments:
        name: nome do usuário
           userid: número de cada usuário
            age: idade do usuário
            estimatedsalary: estimativa do salário do usuário
            gender: gênero do usuário
            purchased: se o item foi comprado ou  não pelo usuário
            
        """

        self.name=name
        self.userid= userid
        self.age = age
        self.estimatedsalary = estimatedsalary
        self.gender = gender
        self.purchased = purchased
        

        # se não for informada, será o data exata da inserção no banco
        if data_insercao:
            self.data_insercao = data_insercao