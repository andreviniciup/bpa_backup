import hashlib
from flask import request, render_template, redirect, url_for, session
from app import app
from app.utils.bpa_controller import BPAController
from app.utils.bpa_view import BPAView, send_file
from app.services.bpa_service import BPAService

# Instancia controlador e view
bpa_controller = BPAController()
bpa_view = BPAView()

# Credenciais fixas
USERNAME_PADRAO = "ADMIN"
SENHA_PADRAO_MD5 = hashlib.md5("ADMIN".encode()).hexdigest()

# Rota que redireciona para a página de login
@app.route("/", methods=["GET", "POST"])
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form['username'].strip().upper()
        senha = request.form['password'].strip()
        senha_md5 = hashlib.md5(senha.encode()).hexdigest()
        
        # Verifica credenciais fixas
        if login == USERNAME_PADRAO and senha_md5 == SENHA_PADRAO_MD5:
            session['username'] = login
            session['nom_usuario'] = "Administrador"  # Nome fixo para o usuário
            session['cod_usuario'] = 1  # Código fixo do usuário
            session['cod_tipo_usuario'] = 1  # Tipo fixo de usuário
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


