from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import declarative_base, sessionmaker

# Cria a conexão com o banco de dados SQLite local
DATABASE_URL = "sqlite:///rpg.db"

# O engine é o motor que gerencia a comunicação com o arquivo .db
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# O sessionmaker é o que permite abrir "sessões" para salvar ou buscar dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# A classe Base será herdada por todos os modelos para o SQLAlchemy reconhecê-los
Base = declarative_base()


def ensure_database_schema():
    """Cria as tabelas e adiciona colunas novas em bancos já existentes."""
    Base.metadata.create_all(bind=engine)

    inspector = inspect(engine)
    if "personagens" not in inspector.get_table_names():
        return

    columns = {column["name"] for column in inspector.get_columns("personagens")}
    if "pericias" not in columns:
        with engine.begin() as connection:
            connection.execute(text("ALTER TABLE personagens ADD COLUMN pericias VARCHAR"))


def get_db():
    """Função utilitária para abrir e fechar a sessão do banco com segurança"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
