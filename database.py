from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Usando SQLite com arquivo local
SQLALCHEMY_DATABASE_URL = "sqlite:///./todo_tasks.db"

# Cria o engine do banco de dados
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}  # necessário para SQLite
)

# Cria a sessão de banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para os modelos
Base = declarative_base()

# Função para inicializar o banco de dados
def init_db():
    """
    Cria as tabelas no banco de dados.
    Chamado no main.py ao iniciar a aplicação.
    """
    Base.metadata.create_all(bind=engine)