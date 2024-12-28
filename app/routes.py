from flask import request, render_template, redirect, url_for, session
from app import app, db
from app.models import User
from app.utils.bpa_controller import BPAController
from app.utils.bpa_view import BPAView

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
        # Verifica as credenciais no banco de dados
        user = User.query.filter_by(login=login, senha=senha).first()
        if user:
            session['username'] = login
            session['nom_usuario'] = user.nom_usuario  # Armazena o nome do usuário na sessão
            return redirect(url_for('formulario_bpa'))
        else:
            return render_template('login.html', error='Credenciais inválidas')
    return render_template('login.html')

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('username', None)
    session.pop('nom_usuario', None)  # Remove o nome do usuário da sessão
    return redirect(url_for('login'))

# Rota que apenas coordena o fluxo entre controller e view
@app.route("/formulario_bpa", methods=["GET", "POST"])
def formulario_bpa():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == "POST":
        return bpa_controller.process_form(request.form)
    return bpa_view.render_form()