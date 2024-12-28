from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuração da URI de conexão com o banco de dados PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://desenv:desenv123@198.58.104.92:5432/testeBPA'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define a chave secreta para a aplicação Flask
app.secret_key = '12321444545453657455442345fdgdcbvxcxdvvbxbf345254546'  # Substituir por uma chave mais segura em produção

from app import routes