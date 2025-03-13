from flask import Flask

app = Flask(__name__)


# Define a chave secreta para a aplicação Flask
app.secret_key = '12321444545453657455442345fdgdcbvxcxdrifjvvvbxbf345254546'  

from app import routes