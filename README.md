# API de Tarefas (To-Do List)

Uma API RESTful simples para gerenciar tarefas com autenticação de usuários, desenvolvida com FastAPI e SQLite.

## Tecnologias Utilizadas

- Python 3.7+
- FastAPI
- SQLAlchemy
- SQLite
- JWT para autenticação
- Pydantic para validação de dados

## Instalação

1. Clone este repositório
2. Crie um ambiente virtual: `python -m venv venv`
3. Ative o ambiente virtual:
   - No Windows: `venv\\Scripts\\activate`
   - No Linux/Mac: `source venv/bin/activate`
4. Instale as dependências: `pip install -r requirements.txt`

## Como Rodar

Após instalar as dependências, execute:

```bash
uvicorn main:app --reload
```

A API estará disponível em `http://127.0.0.1:8000`

A documentação automática estará disponível em `http://127.0.0.1:8000/docs`

## Endpoints da API

| Método | Rota | Descrição | Exemplo de Request/Response |
|--------|------|-----------|-------------------------------|
| POST | `/api/register` | Registra um novo usuário | Request: `{"name": "João", "email": "joao@email.com", "password": "senha123"}`<br>Response: `{"id": 1, "name": "João", "email": "joao@email.com", "created_at": "2023-01-01T00:00:00"}` |
| POST | `/api/login` | Realiza login e retorna token JWT | Request: `{"email": "joao@email.com", "password": "senha123"}`<br>Response: `{"access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...", "token_type": "bearer"}` |
| POST | `/api/tasks` | Cria uma nova tarefa (protegido) | Request: `{"title": "Estudar FastAPI", "description": "Aprender sobre rotas e dependências", "priority": 2}`<br>Response: `{"id": 1, "title": "Estudar FastAPI", "description": "Aprender sobre rotas e dependências", "priority": 2, "completed": false, "created_at": "2023-01-01T00:00:00", "updated_at": "2023-01-01T00:00:00", "owner_id": 1}` |
| GET | `/api/tasks` | Lista todas as tarefas do usuário (protegido) | Response: `[{"id": 1, "title": "Estudar FastAPI", ...}]` |
| GET | `/api/tasks/{id}` | Obtém uma tarefa específica (protegido) | Response: `{"id": 1, "title": "Estudar FastAPI", ...}` |
| PUT | `/api/tasks/{id}` | Atualiza uma tarefa (protegido) | Request: `{"title": "Estudar FastAPI avançado", "completed": true}`<br>Response: `{"id": 1, "title": "Estudar FastAPI avançado", "completed": true, ...}` |
| DELETE | `/api/tasks/{id}` | Deleta uma tarefa (protegido) | Response: 204 No Content |

## Observações

- O token JWT deve ser enviado no header `Authorization` como `Bearer <token>` nas rotas protegidas.
- A senha mínima é de 6 caracteres (validação feita no frontend/backend).
- O banco de dados SQLite é criado automaticamente como `todo_tasks.db` na raiz do projeto.
- A chave secreta JWT está hardcoded por simplicidade, mas em produção deve ser gerada aleatoriamente e armazenada em variáveis de ambiente.