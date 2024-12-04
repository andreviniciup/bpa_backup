from flask import request
from app import app
from app.utils.bpa_controller import BPAController
from app.utils.bpa_view import BPAView

# Instancia controlador e view
bpa_controller = BPAController()
bpa_view = BPAView()

# Rota que apenas coordena o fluxo entre controller e view
@app.route("/", methods=["GET", "POST"])
def formulario_bpa():
    if request.method == "POST":
        return bpa_controller.process_form(request.form)
    return bpa_view.render_form()