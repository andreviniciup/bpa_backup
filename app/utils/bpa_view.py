from flask import render_template, send_file

# Classe responsável pela apresentação (interface com usuário)
class BPAView:
    @staticmethod
    def render_form(error=None):
        """
        Renderiza o formulário HTML
        Args:
            error: mensagem de erro opcional para exibir ao usuário
        Returns:
            Página HTML renderizada
        """
        return render_template("bpa.html", error=error)
    
    @staticmethod
    def send_file(memoria, tipo_relatorio):
        """
        Prepara o arquivo para download
        Args:
            memoria: buffer contendo o arquivo
            tipo_relatorio: tipo do relatório para nome do arquivo
        Returns:
            Resposta HTTP para download do arquivo
        """
        return send_file(
            memoria,
            as_attachment=True,
            download_name=f"resultado_bpa_{tipo_relatorio}.txt",
            mimetype="text/plain"
        )