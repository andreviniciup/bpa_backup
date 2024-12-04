from app.utils.bpa_service import BPAService
from app.utils.bpa_view import BPAView

# Classe que coordena o fluxo entre a lógica de negócio (Service) e a apresentação (View)
class BPAController:
    def __init__(self):
        # Inicializa os objetos necessários
        self.service = BPAService()
        self.view = BPAView()
    
    def process_form(self, form_data):
        """
        Processa os dados do formulário, coordenando a geração do arquivo e sua apresentação
        Args:
            form_data: dados do formulário enviado pelo usuário
        Returns:
            Resposta HTTP apropriada (arquivo para download ou página com erro)
        """
        try:
            # Obtém o tipo de relatório do formulário
            tipo_relatorio = form_data.get("tipo_relatorio")
            # Solicita a geração do arquivo ao serviço
            memoria = self.service.generate_bpa_file(tipo_relatorio)
            # Envia o arquivo gerado para download
            return self.view.send_file(memoria, tipo_relatorio)
        except ValueError as e:
            # Erro de validação (tipo de relatório inválido)
            return self.view.render_form(error=str(e))
        except Exception as e:
            # Outros erros inesperados
            return self.view.render_form(error=f"Erro ao gerar arquivo: {str(e)}")