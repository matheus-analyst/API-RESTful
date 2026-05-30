from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
import models, schemas, auth, database

# Criando um roteador para organizar as rotas
router = APIRouter()

def get_db():
    """
    Dependência que fornece uma sessão de banco de dados.
    Garante que a sessão seja fechada após o uso.
    """
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Rotas de autenticação
@router.post("/register", response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Registra um novo usuário no sistema.
    Verifica se o email já existe e cria o hash da senha.
    """
    # Verifica se o email já está cadastrado
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já cadastrado"
        )
    
    # Cria o hash da senha
    hashed_password = auth.get_password_hash(user.password)
    
    # Cria o novo usuário
    db_user = models.User(
        name=user.name,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # Formata a data para string
    db_user.created_at = db_user.created_at.isoformat()
    
    return db_user

@router.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    """
    Realiza login e retorna um token JWT.
    Verifica email e senha antes de gerar o token.
    """
    # Busca o usuário pelo email
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    # Verifica a senha
    if not auth.verify_password(user.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    # Gera o token JWT
    access_token = auth.create_access_token(data={"sub": db_user.email})
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

# Função auxiliar para obter o usuário atual a partir do token
def get_current_user(db: Session = Depends(get_db), token: str = Depends(auth.oauth2_scheme)):
    """
    Extrai o usuário do token JWT.
    Levanta exceção se o token for inválido ou expirado.
    """
    try:
        payload = jwt.decode(token, auth.settings.SECRET_KEY, algorithms=[auth.settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Não foi possível validar as credenciais",
                headers={"WWW-Authenticate": "Bearer"}
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Não foi possível validar as credenciais",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    user = db.query(models.User).filter(models.User.email == email).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário não encontrado",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    return user

# Rotas de tarefas (protegidas)
@router.post("/tasks", response_model=schemas.TaskOut, status_code=status.HTTP_201_CREATED)
def create_task(
    task: schemas.TaskCreate, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
):
    """
    Cria uma nova tarefa para o usuário autenticado.
    O título é obrigatório.
    """
    if not task.title.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Título da tarefa é obrigatório"
        )
    
    db_task = models.Task(
        title=task.title,
        description=task.description,
        priority=task.priority,
        owner_id=current_user.id
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    
    # Formata as datas para string
    db_task.created_at = db_task.created_at.isoformat()
    db_task.updated_at = db_task.updated_at.isoformat()
    
    return db_task

@router.get("/tasks", response_model=list[schemas.TaskOut])
def read_tasks(
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
):
    """
    Retorna todas as tarefas do usuário autenticado.
    """
    tasks = db.query(models.Task).filter(models.Task.owner_id == current_user.id).all()
    
    # Formata as datas para string
    for task in tasks:
        task.created_at = task.created_at.isoformat()
        task.updated_at = task.updated_at.isoformat()
    
    return tasks

@router.get("/tasks/{task_id}", response_model=schemas.TaskOut)
def read_task(
    task_id: int, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
):
    """
    Retorna uma tarefa específica do usuário autenticado.
    """
    task = db.query(models.Task).filter(models.Task.id == task_id, models.Task.owner_id == current_user.id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tarefa não encontrada"
        )
    
    # Formata as datas para string
    task.created_at = task.created_at.isoformat()
    task.updated_at = task.updated_at.isoformat()
    
    return task

@router.put("/tasks/{task_id}", response_model=schemas.TaskOut)
def update_task(
    task_id: int, 
    task_update: schemas.TaskUpdate, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
):
    """
    Atualiza uma tarefa existente do usuário autenticado.
    Pode atualizar título, descrição, prioridade ou status de conclusão.
    """
    db_task = db.query(models.Task).filter(models.Task.id == task_id, models.Task.owner_id == current_user.id).first()
    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tarefa não encontrada"
        )
    
    # Atualiza apenas os campos fornecidos
    if task_update.title is not None:
        if not task_update.title.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Título da tarefa não pode ser vazio"
            )
        db_task.title = task_update.title
    
    if task_update.description is not None:
        db_task.description = task_update.description
    
    if task_update.priority is not None:
        if task_update.priority not in [1, 2, 3]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Prioridade deve ser 1 (baixa), 2 (média) ou 3 (alta)"
            )
        db_task.priority = task_update.priority
    
    if task_update.completed is not None:
        db_task.completed = task_update.completed
    
    db_task.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_task)
    
    # Formata as datas para string
    db_task.created_at = db_task.created_at.isoformat()
    db_task.updated_at = db_task.updated_at.isoformat()
    
    return db_task

@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
):
    """
    Deleta uma tarefa específica do usuário autenticado.
    """
    task = db.query(models.Task).filter(models.Task.id == task_id, models.Task.owner_id == current_user.id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tarefa não encontrada"
        )
    
    db.delete(task)
    db.commit()
    
    # Retorna 204 No Content sem corpo
    return