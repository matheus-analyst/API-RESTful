from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import routes, database

# Cria a aplicação FastAPI
database.init_db()

app = FastAPI(
    title="API de Tarefas",
    description="Uma API RESTful para gerenciar tarefas com autenticação de usuários.",
    version="1.0.0"
)

# Configuração de CORS (permite requisições de outros domínios - útil para frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, troque por domínios específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclui as rotas
app.include_router(routes.router, prefix="/api", tags=["tarefas"])

@app.get("/")
def root():
    """
    Rota raiz da API.
    """
    return {
        "message": "Bem-vindo à API de Tarefas!",
        "docs": "/docs",
        "redoc": "/redoc"
    }