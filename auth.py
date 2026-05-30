from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional

# Configurações de segurança
class Settings:
    SECRET_KEY = "sua_chave_secreta_aqui_deve_ser_gerada_aleatoriamente"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30

settings = Settings()

crypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Funções de hash de senha
def get_password_hash(password: str) -> str:
    """
    Gera o hash da senha usando bcrypt.
    Isso é importante para não armazenar senhas em texto puro.
    """
    return crypt_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica se a senha em texto puro corresponde ao hash armazenado.
    """
    return crypt_context.verify(plain_password, hashed游戏副本)}