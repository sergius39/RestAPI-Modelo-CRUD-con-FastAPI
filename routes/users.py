from fastapi import APIRouter
from config.db import conn
from models.user import users
from schemas.user import User
from cryptography.fernet import Fernet
from sqlalchemy import select

key=Fernet.generate_key()
f=Fernet(key)

user=APIRouter()

@user.get('/users')
def get_user():
    users_data=[]
    for user_row in conn.execute(users.select()).fetchall():
        user_dic={
            "id":user_row.id,
            "name":user_row.name,
            "email":user_row.email,
        }
        users_data.append(user_dic)
    return users_data

@user.post('/users')
def create_user(user:User):
    new_user={"name":user.name, "email":user.email, "password": f.encrypt(user.password.encode('UTF-8'))
    }
    print(new_user)
    conn.execute(users.insert().values(new_user))
    conn.commit()
    return "Usuario creado correctamente"

@user.put('/users')
def update_user(id: int, user:User):
    conn.execute(users.update().value(name=user.name, email=user.email, password=f.encrypt(user.password.encode('utf-8'))).where(users.c.id==id))
    return "Usuario actualizado"

@user.delete('/users')
def delete_user(id:int):
    conn.execute(users.delete().where(users.c.id==id))
    conn.commit()
    return 'Usuario: ',id,' eliminado'



