# mapeamento completo de dados
DATA_MAPPING = {
    "prd-ident": {"type": "NUM(002)",
                   "table": "padrao",
                   "column": "", 
                    "predefinido": "03"},

    "prd-cnes": {"type": "NUM(007)", 
                "table": "estabelecimento", 
                "column": "num_cnes", 
                "check": True, 
                "check_table": "paciente",
                "check_column": "nom_paciente"},


    "prd-cmp": {"type": "NUM(006)",
                "table": "competencia", 
                "column": "cod_competencia", 
                "check": True, 
                "check_table": "paciente", 
                "check_column": "nom_paciente"},
    
    # Dados do médico
    "prd-cnsmed": {"type": "NUM(015)", 
                   "table": "medico", 
                   "column": "num_cns", 
                   "check": True, 
                   "check_table": "paciente", 
                   "check_column": "nom_paciente"},

    "prd-cbo": {"type": "ALFA(006)", 
                "table": "medico", 
                "column": "num_cbo", 
                "check": True, 
                "check_table": "paciente", 
                "check_column": "nom_paciente"},
    
    # Dados do atendimento
    "prd-dtaten": {"type": "NUM(008)", 
                   "table": "atendimento", 
                   "column": "data_atendimento", 
                   "check": True, 
                   "check_table": "paciente", 
                   "check_column": "nom_paciente"},

    "prd-flh": {"type": "NUM(003)", 
                "table": "atendimento", 
                "column": "num_folha", 
                "check": True, 
                "check_table": "paciente", 
                "check_column": "nom_paciente"},

    "prd-seq": {"type": "NUM(002)", 
                "table": "atendimento", 
                "column": "num_sequencia", 
                "check": True, 
                "check_table": "paciente", 
                "check_column": "nom_paciente"},

    "prd-pa": {"type": "NUM(010)", 
               "table": "procedimento", 
               "column": "cod_procedimento", 
               "check": True, 
               "check_table": "paciente", 
               "check_column": "nom_paciente"},
    
    # Dados do paciente
    "prd-cnspac": {"type": "NUM(015)", 
                   "table": "paciente", 
                   "column": "num_cns", 
                   "check": True, 
                   "check_table": "paciente", 
                   "check_column": "nom_paciente"},

    "prd-sexo": {"type": "ALFA(001)", 
                 "table": "paciente", 
                 "column": "tip_sexo", 
                 "check": True, 
                 "check_table": "paciente", 
                 "check_column": "nom_paciente"},

    "prd-ibge": {"type": "NUM(007)", 
                 "table": "paciente", 
                 "column": "cod_municipio", 
                 "check": True, 
                 "check_table": "municipio", 
                 "check_column": "cod_ibge"},

    "prd-cid": {"type": "ALFA(004)", 
                "table": "atendimento", 
                "column": "cod_cid", 
                "check": True, 
                "check_table": "cid", 
                "check_column": "cod_cid"},

    "prd-idade": {"type": "NUM(003)", 
                  "table": "paciente", 
                  "column": "idade", 
                  "check": True, 
                  "check_table": "paciente", 
                  "check_column": "nom_paciente"},

    "prd-qt": {"type": "NUM(006)", 
               "table": "atendimento", 
               "column": "qtd_procedimento", 
               "check": True, 
               "predefinido": "000001"},

    "prd-caten": {"type": "NUM(002)", 
                  "table": "atendimento", 
                  "column": "cod_tipo_atendimento", 
                  "check": True, 
                  "check_table": "paciente", 
                  "check_column": "nom_paciente"},

    "prd-naut": {"type": "NUM(013)", 
                 "table": "atendimento", 
                 "column": "num_autorizacao", 
                 "check": True, 
                 "check_table": "paciente", 
                 "check_column": "nom_paciente"},
    
    # Nacionalidade e Identificação
    "prd-org": {"type": "ALFA(003)",
                 "table": "paciente", 
                 "column": "cod_nacionalidade", 
                 "check": True, 
                 "check_table": "nacionalidade", 
                 "check_column": "sigla", 
                 "predefinido": "BR"},

    "prd-nmpac": {"type": "ALFA(030)", 
                  "table": "paciente", 
                  "column": "nom_paciente",
                  "check": True},

    "prd-dtnasc": {"type": "NUM(008)", 
                   "table": "paciente", 
                   "column": "data_nascimento", 
                   "check": True},

    "prd-raca": {"type": "NUM(002)", 
                 "table": "paciente", 
                 "column": "cod_raca", 
                 "check": True, 
                 "check_table": "raca", 
                 "check_column": "cod_raca"},

    "prd-etnia": {"type": "NUM(004)", 
                  "table": "paciente", 
                  "column": "cod_etnia", 
                  "check": True, 
                  "check_table": "etnia", 
                  "check_column": "cod_etnia", 
                  "predefinido": "    "},

    "prd-nac": {"type": "NUM(003)", 
                "table": "paciente", 
                "column": "cod_nacionalidade", 
                "check": True, 
                "check_table": "nacionalidade",
                "check_column": "cod_nacionalidade", 
                "predefinido": "055"},
    
    # Serviço e Classificação
    "prd-srv": {"type": "NUM(003)", 
                "table": "atendimento", 
                "column": "cod_servico", 
                "check": True,
                "predefinido": "001"},

    "prd-clf": {"type": "NUM(003)",
                 "table": "atendimento", 
                 "column": "cod_classificacao", 
                 "check": True, 
                 "predefinido": "001"},
    
    # Equipe
    "prd-equipe-seq": {"type": "NUM(008)", 
                       "table": "equipe", 
                       "column": "num_sequencia", 
                       "check": True, 
                       "predefinido": "00000001"},

    "prd-equipe-area": {"type": "NUM(004)", 
                        "table": "equipe", 
                        "column": "num_area", 
                        "check": True, 
                        "predefinido": "0001"},
    
    # Dados do prestador
    "prd-cnpj": {"type": "NUM(014)", 
                 "table": "estabelecimento", 
                 "column": "num_cnpj", 
                 "check": True},
    
    # Endereço do paciente
    "prd-cep-pcnte": {"type": "NUM(008)", 
                      "table": "endereco_paciente", 
                      "column": "num_cep", 
                      "check": True},

    "prd-lograd-pcnte": {"type": "NUM(003)",
                          "table": "endereco_paciente",
                          "column": "tip_logradouro",
                          "check": True, 
                          "check_table": "tipo_logradouro", 
                          "check_column": "cod_tipo"},

    "prd-end-pcnte": {"type": "ALFA(030)", 
                      "table": "endereco_paciente", 
                      "column": "des_logradouro", 
                      "check": True},

    "prd-compl-pcnte": {"type": "ALFA(010)", 
                        "table": "endereco_paciente", 
                        "column": "des_complemento", 
                        "check": True},

    "prd-num-pcnte": {"type": "ALFA(005)", 
                      "table": "endereco_paciente", 
                      "column": "num_endereco", 
                      "check": True},
    "prd-bairro-pcnte": {"type": "ALFA(030)", 
                         "table": "endereco_paciente", 
                         "column": "des_bairro", 
                         "check": True},
    
    # Contato do paciente
    "prd-ddtel-pcnte": {"type": "NUM(011)", 
                        "table": "contato_paciente", 
                        "column": "num_telefone", 
                        "check": True},

    "prd-email-pcnte": {"type": "ALFA(040)",
                         "table": "contato_paciente", 
                         "column": "des_email", 
                         "check": True},
    
    # INE (Identificador Nacional de Equipes)
    "prd-ine": {"type": "NUM(010)", 
                "table": "equipe", 
                "column": "num_ine", 
                "check": True, 
                "predefinido": "0000000001"},
    
    # Finalizador de registro
    "prd-fim": {"type": "ALFA(002)", 
                "table": "padrao", 
                "column": "", 
                "predefinido": "\r\n"}
}