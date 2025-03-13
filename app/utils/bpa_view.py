from flask import render_template, send_file

# Classe responsável pela apresentação (interface com usuário)
class BPAView:
    @staticmethod
    def render_form(error=None, form_data=None):
        """
        Renderiza o formulário HTML
        Args:
            error: mensagem de erro opcional para exibir ao usuário
        Returns:
            Página HTML renderizada
        """
        return render_template("bpa.html", error=error, form_data=form_data)
    
    @staticmethod
    def send_file(memoria, tipo_relatorio):
        print(f"Tamanho do arquivo gerado: {memoria.getbuffer().nbytes} bytes")  # Debug
        return send_file(
            memoria,
            as_attachment=True,
            download_name=f"resultado_bpa_{tipo_relatorio}.txt",
            mimetype="text/plain"
        )