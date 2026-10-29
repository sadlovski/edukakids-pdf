import os
import zipfile
import io
import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

st.set_page_config(page_title="Gerador Kit EdukaKids", page_icon="🎨", layout="centered")

st.title("🎨 Gerador Automático - Kit EdukaKids")
st.markdown("Crie e ajuste seus módulos de atividades infantis de forma rápida, sem mexer em códigos.")

# Configurações do Módulo na Barra Lateral
st.sidebar.header("📁 Configurações do Módulo")
nome_modulo = st.sidebar.text_input("Nome da Pasta do Módulo", "01-Alfabetizacao-Divertida")
quantidade = st.sidebar.slider("Número de Fichas", min_value=1, max_value=30, value=5)

st.subheader("📝 Conteúdo das Fichas")

fichas_data = []
for i in range(1, int(quantidade) + 1):
    with st.expander(f"Ficha {i:02d}", expanded=(i == 1)):
        col1, col2 = st.columns([1, 2])
        with col1:
            num = st.text_input(f"Identificador #{i}", value=f"Ficha {i:02d}", key=f"num_{i}")
        with col2:
            titulo = st.text_input(f"Título #{i}", value=f"Atividade Divertida {i}", key=f"titulo_{i}")
        instrucao = st.text_area(f"Instrução da Ficha #{i}", value=f"Encontre e trace o caminho correto da atividade {i}.", key=f"instr_{i}")
        fichas_data.append((num, titulo, instrucao))

if st.button("🚀 Gerar e Baixar Pacote de PDFs", type="primary"):
    buffer_zip = io.BytesIO()
    
    with zipfile.ZipFile(buffer_zip, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for num, titulo, instrucao in fichas_data:
            pdf_buffer = io.BytesIO()
            
            doc = SimpleDocTemplate(pdf_buffer, pagesize=A4, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
            story = []
            
            logo_path = "EdukakidsLogo.jpg"
            if os.path.exists(logo_path):
                story.append(Image(logo_path, width=90, height=90))
                story.append(Spacer(1, 10))
            
            styles = getSampleStyleSheet()
            info_style = ParagraphStyle('InfoStyle', parent=styles['Normal'], fontSize=10, textColor=colors.black, alignment=0)
            title_style = ParagraphStyle('TitleStyle', parent=styles['Heading1'], fontSize=18, textColor=colors.HexColor('#1d3557'), alignment=1, spaceAfter=15)
            body_style = ParagraphStyle('BodyStyle', parent=styles['Normal'], fontSize=12, textColor=colors.HexColor('#457b9d'), alignment=1, spaceAfter=30)
            
            story.append(Paragraph("<b>Nome:</b> ____________________________________ &nbsp;&nbsp;&nbsp;&nbsp; <b>Data:</b> ___/___/______", info_style))
            story.append(Spacer(1, 30))
            story.append(Paragraph(f"<b>{num}: {titulo}</b>", title_style))
            story.append(Paragraph(instrucao, body_style))
            
            doc.build(story)
            
            pdf_filename = f"{nome_modulo}/{num.lower().replace(' ', '-')}.pdf"
            zip_file.writestr(pdf_filename, pdf_buffer.getvalue())
    
    buffer_zip.seek(0)
    st.success("🎉 Todas as fichas foram geradas com sucesso!")
    st.download_button(
        label="📥 Baixar ZIP com o Módulo Completo",
        data=buffer_zip,
        file_name=f"{nome_modulo}.zip",
        mime="application/zip"
    )