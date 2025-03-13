from sqlalchemy import text
from app import db

def valida_login(login, senha_md5):
    sql = text("""
        SELECT U.COD_USUARIO, U.NOM_USUARIO, U.COD_TIPO_USUARIO, U.STATUS 
        FROM usuario U 
        WHERE U.LOGIN = :login AND U.SENHA = :senha AND U.STATUS='A';
    """)
    result = db.session.execute(sql, {'login': login, 'senha': senha_md5})
    return result.fetchone()
