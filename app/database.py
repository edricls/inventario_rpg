from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Cria a conexão com o banco de dados SQLite local
DATABASE_URL = "sqlite:///rpg.db"

# O engine é o motor que gerencia a comunicação com o arquivo .db
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# O sessionmaker é o que permite abrir "sessões" para salvar ou buscar dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# A classe Base será herdada por todos os modelos para o SQLAlchemy reconhecê-los
Base = declarative_base()

def get_db():
    """Função utilitária para abrir e fechar a sessão do banco com segurança"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

DATABASE_URL = "sqlite:///rpg.db"