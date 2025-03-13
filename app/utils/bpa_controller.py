import logging
from app.services.bpa_service import BPAService
from app.utils.bpa_view import BPAView

class BPAController:
    def __init__(self):
        self.service = BPAService()
        self.view = BPAView()
        # Configuração de logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            filename='bpa_system.log'
        )
        self.logger = logging.getLogger('bpa_controller')

    def process_form(self, form_data):
        """
        Processa os dados do formulário e gera o arquivo BPA.
        
        Args:
            form_data (dict): Dados enviados pelo usuário.
        
        Returns:
            Resposta HTTP apropriada (arquivo para download ou página com erro)
        """
        self.logger.info(f"Iniciando processamento de formulário BPA. Competência: {form_data.get('year_month')}")
        
        try:
            # Validações de entrada
            year_month = form_data.get("year_month")
            if not year_month:
                self.logger.warning("Tentativa de submissão sem competência")
                return self.view.render_form(
                    error="O campo 'competência' é obrigatório.",
                    form_data=form_data
                )

            # Certifique-se de que year_month está no formato correto (YYYYMM)
            if len(year_month) != 6 or not year_month.isdigit():
                self.logger.warning(f"Formato de competência inválido: {year_month}")
                return self.view.render_form(
                    error="A competência deve estar no formato AAAAMM (exemplo: 202311).",
                    form_data=form_data
                )

            tipo_relatorio = form_data.get("tipo_relatorio", "individualizada")
            if tipo_relatorio not in ["individualizada", "consolidado"]:
                self.logger.warning(f"Tipo de relatório inválido: {tipo_relatorio}")
                return self.view.render_form(
                    error="Tipo de relatório inválido. Use 'individualizada' ou 'consolidado'.",
                    form_data=form_data
                )

            self.logger.info(f"Gerando arquivo BPA {tipo_relatorio} para competência {year_month}")
            memoria = self.service.generate_bpa_file(year_month, tipo_relatorio)
            
            self.logger.info(f"Arquivo BPA gerado com sucesso. Enviando para download.")
            return self.view.send_file(memoria, tipo_relatorio)

        except ValueError as e:
            # Erros de validação específicos
            self.logger.warning(f"Erro de validação: {str(e)}")
            return self.view.render_form(
                error=str(e),
                form_data=form_data
            )
        except ConnectionError as e:
            # Erros de conexão com banco de dados
            self.logger.error(f"Erro de conexão: {str(e)}")
            return self.view.render_form(
                error="Não foi possível conectar ao banco de dados. Tente novamente mais tarde.",
                form_data=form_data
            )
        except Exception as e:
            # Outros erros inesperados
            self.logger.error(f"Erro inesperado: {str(e)}", exc_info=True)
            return self.view.render_form(
                error="Ocorreu um erro inesperado. Por favor, entre em contato com o suporte técnico.",
                form_data=form_data
            )