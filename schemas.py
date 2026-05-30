from pydantic import BaseModel, EmailStr
from typing import Optional

# Esquema para criação de usuário
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

# Esquema para retorno de usuário (sem senha)
class UserOut(BaseModel):
    id: int
    name: str
    email: str
    created_at: str

    class Config:
        orm_mode = True

# Esquema para login
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Esquema para criação de tarefa
class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    priority: int = 1  # padrão: baixa prioridade

# Esquema para atualização de tarefa
class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[int] = None
    completed: Optional[bool] = None

# Esquema para retorno de tarefa
class TaskOut(BaseModel):
    id: int
    title: str
    description: Optional[str]
    priority: int
    completed: bool
    created_at: str
    updated_at: str
    owner_id: int

    class Config:
        orm_mode = True