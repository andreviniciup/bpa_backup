'''from sqlalchemy import text
from app import db

def get_dashboard_data():
    sql = text("""
        SELECT
            QA.seq_quantitativo_atendimento,
            QA.num_qtde_admissao_24hs,
            QA.num_qtde_alta_24hs,
            QA.num_qtde_ala_amarela_atual,
            QA.num_qtde_ala_vermelha_atual,
            QA.num_qtde_ala_azul_atual,
            QA.num_qtde_sala_medicacao_atual,
            QA.num_tempo_medio_atendimento_24hs,
            QA.num_qtde_pacientes_aguardam_acolhimento_atual,
            QA.num_tempo_medio_para_triagem_24hs,
            QA.num_tempo_medio_para_atendimento_24hs
        FROM quantitativo_atendimento QA 
        ORDER BY QA.seq_quantitativo_atendimento DESC LIMIT 1;
    """)
    result = db.session.execute(sql)
    return result.fetchone()'''