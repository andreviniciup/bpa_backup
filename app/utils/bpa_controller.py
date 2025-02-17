from app.services.bpa_service import BPAService
from app.utils.bpa_view import BPAView

class BPAController:
    def __init__(self):
        self.service = BPAService()
        self.view = BPAView()

    def process_form(self, form_data):
        """
        Processa os dados do formulário e gera o arquivo BPA.
        
        Args:
            form_data (dict): Dados enviados pelo usuário.
        
        Returns:
            Resposta HTTP apropriada (arquivo para download ou página com erro)
        """
        try:
            year_month = form_data.get("year_month")
            if not year_month:
                raise ValueError("O campo 'year_month' é obrigatório.")

            tipo_relatorio = form_data.get("tipo_relatorio")
            memoria = self.service.generate_bpa_file(year_month, tipo_relatorio)

            return self.view.send_file(memoria, tipo_relatorio)

        except ValueError as e:
            return self.view.render_form(error=str(e))
        except Exception as e:
            return self.view.render_form(error=f"Erro ao gerar arquivo: {str(e)}")
