import hashlib
from flask import request, render_template, redirect, url_for, session
from app import app, db
from app.models import User
from app.utils.bpa_controller import BPAController
from app.utils.bpa_view import BPAView
from app.utils.auth import valida_login  
from app.utils.dashboard import get_dashboard_data 

# Instancia controlador e view
bpa_controller = BPAController()
bpa_view = BPAView()

# Rota que redireciona para a página de login
@app.route("/", methods=["GET", "POST"])
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form['username']
        senha = request.form['password']
        # Encripta a senha com MD5
        senha_md5 = hashlib.md5(senha.encode()).hexdigest()
        # Verifica as credenciais no banco de dados
        user = valida_login(login, senha_md5)
        if user:
            session['username'] = login
            session['nom_usuario'] = user.nom_usuario  # Armazena o nome do usuário na sessão
            session['cod_usuario'] = user.cod_usuario  # Armazena o código do usuário na sessão
            session['cod_tipo_usuario'] = user.cod_tipo_usuario  # Armazena o tipo do usuário na sessão
            return redirect(url_for('menu'))
        else:
            return render_template('login.html', error='Credenciais inválidas')
    return render_template('login.html')

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('username', None)
    session.pop('nom_usuario', None)  # Remove o nome do usuário da sessão
    session.pop('cod_usuario', None)  # Remove o código do usuário da sessão
    session.pop('cod_tipo_usuario', None)  # Remove o tipo do usuário da sessão
    return redirect(url_for('login'))

@app.route('/menu')
def menu():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('menu.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    data = get_dashboard_data()
    return render_template('dashboard.html', data=data)

@app.route("/formulario_bpa", methods=["GET", "POST"])
def formulario_bpa():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == "POST":
        return bpa_controller.process_form(request.form)
    return bpa_view.render_form()