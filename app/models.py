"""from app import db

class User(db.Model):
    __tablename__ = 'usuario'
    cod_usuario = db.Column(db.Integer, primary_key=True)
    nom_usuario = db.Column(db.String, unique=True, nullable=False)
    senha = db.Column(db.String(32), nullable=False)
    login = db.Column(db.String(20), unique=True, nullable=False)
    status = db.Column(db.String(1), nullable=False, default='A')
    cod_tipo_usuario = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<User {self.login}>'
    
"""