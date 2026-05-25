# Aqui você vai definir as regras estruturais dos seus dados.
# É onde você diz para o Python como devem ser as tabelas dentro do banco de dados.
from app.database import Base
from sqlalchemy import Column, Integer, String


class Personagem(Base):
    __tablename__ = "personagens"  # O nome da tabela no banco de dados

    id = Column(Integer, primary_key=True, index=True)  # ID único para cada personagem
    nome = Column(String, unique=True, index=True)  # Nome do personagem
    classe = Column(String)  # Classe do personagem (ex: combatente, especialista, ocultista)
    nivel = Column(Integer)  # Nível do personagem
    nex = Column(Integer)  # NEX do personagem
    atributos = Column(String)  # Atributos do personagem (força, agilidade, etc.) armazenados como string JSON
    trilha = Column(String)  # Trilha do personagem 
    historia = Column(String)  # História do personagem
    
    

