from flask import render_template, request, send_file
import io
import pandas as pd
from app.utils.bpa_generator import BPAGenerator
from app import app

@app.route("/", methods=["GET", "POST"])
def formulario_bpa():
    if request.method == "POST":
        #obter os dados do formulario
        tipo_relatorio = request.form.get("tipo_relatorio").lower()

        # carregar dados do cabeçalho
        df_cabecalho = pd.read_csv("app/data/cabeçalho.csv", dtype=str)
        header_data = df_cabecalho.iloc[0].to_dict()

        # carregar registros com base no tipo de relatorio
        if tipo_relatorio == "individualizada":
            df_registros = pd.read_csv("app/data/bpa_individualizado.csv", dtype=str)
        elif tipo_relatorio == "consolidado":
            df_registros = pd.read_csv("app/data/bpa_consolidado.csv", dtype=str)
        else:
            return render_template(
                "bpa.html",
                error="Tipo de relatório inválido. Escolha entre 'Consolidado' ou 'Individualizada'."
            )


        # inicializar o gerador BPA
        generator = BPAGenerator()

        # gerar conteúdo BPA em formato de texto
        memoria = io.BytesIO()
        # Escrever cabeçalho
        memoria.write(generator.generate_header(header_data).encode('utf-8'))

        # escrever registros
        for _, row in df_registros.iterrows():
            if tipo_relatorio == "consolidado":
                memoria.write(generator.generate_bpa_c(row).encode('utf-8'))
            elif tipo_relatorio == "individualizada":
                memoria.write(generator.generate_bpa_i(row).encode('utf-8'))

        memoria.seek(0)
        return send_file(
            memoria,
            as_attachment=True,
            download_name=f"resultado_bpa_{tipo_relatorio}.txt",
            mimetype="text/plain"
        )

    return render_template("bpa.html")
