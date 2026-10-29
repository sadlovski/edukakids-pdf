import os
import zipfile
import io
import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.graphics.shapes import Drawing, Rect, Circle, Line, String, Polygon

st.set_page_config(page_title="Gerador Kit EdukaKids", page_icon="🎨", layout="centered")

st.title("🎨 Gerador Automático - Kit EdukaKids")
st.markdown("Painel inteligente para criação automática de apostilas infantis completas com ilustrações.")

# Configurações do Módulo na Barra Lateral
st.sidebar.header("📁 Configurações do Módulo")
nome_modulo = st.sidebar.text_input("Nome da Pasta do Módulo", "01-Alfabetizacao-Divertida")
quantidade = st.sidebar.slider("Número de Fichas", min_value=1, max_value=30, value=6)

st.subheader("📝 Conteúdo e Ilustrações das Fichas")

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

def criar_desenho_tematico(titulo):
    """Gera um elemento gráfico/desenho vetorial divertido baseado no tema da ficha para ocupar a folha em branco"""
    d = Drawing(400, 220)
    # Fundo da caixa de atividade
    d.add(Rect(10, 10, 380, 200, rx=15, ry=15, fillColor=colors.HexColor('#f8f9fa'), strokeColor=colors.HexColor('#457b9d'), strokeWidth=2))
    
    t_lower = titulo.lower()
    if "avião" in t_lower or "a" in t_lower:
        # Desenho estilizado de um carrinho/aviãozinho e caminhos pontilhados
        d.add(Circle(80, 110, 25, fillColor=colors.HexColor('#a8dadc'), strokeColor=colors.HexColor('#1d3557'), strokeWidth=2))
        d.add(String(70, 105, "✈️", fontSize=24))
        d.add(Line(120, 110, 320, 110, strokeColor=colors.HexColor('#e63946'), strokeWidth=3, strokeDashArray=[5, 5]))
        d.add(Circle(330, 110, 15, fillColor=colors.HexColor('#ffb703'), strokeColor=colors.HexColor('#1d3557'), strokeWidth=2))
    elif "escada" in t_lower or "e" in t_lower:
        # Desenho de degraus
        for step in range(4):
            d.add(Rect(80 + (step * 50), 40 + (step * 30), 40, 25, fillColor=colors.HexColor('#ffe8d6'), strokeColor=colors.HexColor('#cb997e'), strokeWidth=2))
        d.add(String(180, 140, "Escalada da Letra E!", fontSize=14, fillColor=colors.HexColor('#1d3557')))
    else:
        # Desenho padrão interativo de formas geométricas e caixas de pintura
        d.add(Rect(60, 70, 80, 80, rx=10, ry=10, fillColor=colors.HexColor('#ffd166'), strokeColor=colors.HexColor('#1d3557'), strokeWidth=2))
        d.add(String(85, 105, "Pinte", fontSize=14, fillColor=colors.HexColor('#1d3557')))
        
        d.add(Rect(160, 70, 80, 80, rx=10, ry=10, fillColor=colors.HexColor('#06d6a0'), strokeColor=colors.HexColor('#1d3557'), strokeWidth=2))
        d.add(String(185, 105, "Trace", fontSize=14, fillColor=colors.HexColor('#1d3557')))
        
        d.add(Rect(260, 70, 80, 80, rx=10, ry=10, fillColor=colors.HexColor('#ef476f'), strokeColor=colors.HexColor('#1d3557'), strokeWidth=2))
        d.add(String(280, 105, "Ligue", fontSize=14, fillColor=colors.HexColor('#1d3557')))
        
    return d

if st.button("🚀 Gerar e Baixar Pacote Completo de PDFs", type="primary"):
    buffer_zip = io.BytesIO()
    
    with zipfile.ZipFile(buffer_zip, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for num, titulo, instrucao in fichas_data:
            pdf_buffer = io.BytesIO()
            
            # Margens otimizadas para caber perfeitamente em 1 página exata
            doc = SimpleDocTemplate(pdf_buffer, pagesize=A4, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
            story = []
            
            # Logo oficial compacta no topo
            logo_path = "EdukakidsLogo.jpg"
            if os.path.exists(logo_path):
                story.append(Image(logo_path, width=70, height=70))
                story.append(Spacer(1, 8))
            
            styles = getSampleStyleSheet()
            info_style = ParagraphStyle('InfoStyle', parent=styles['Normal'], fontSize=10, textColor=colors.black, alignment=0)
            title_style = ParagraphStyle('TitleStyle', parent=styles['Heading1'], fontSize=16, textColor=colors.HexColor('#1d3557'), alignment=1, spaceAfter=8)
            body_style = ParagraphStyle('BodyStyle', parent=styles['Normal'], fontSize=11, textColor=colors.HexColor('#457b9d'), alignment=1, spaceAfter=15)
            
            # Linha de Nome e Data
            story.append(Paragraph("<b>Nome:</b> _________________________________________________ &nbsp;&nbsp; <b>Data:</b> ___/___/______", info_style))
            story.append(Spacer(1, 15))
            
            # Título e Instrução
            story.append(Paragraph(f"<b>{num}: {titulo}</b>", title_style))
            story.append(Paragraph(instrucao, body_style))
            story.append(Spacer(1, 10))
            
            # Inserção automática do desenho temático na folha
            story.append(criar_desenho_tematico(titulo))
            
            doc.build(story)
            
            pdf_filename = f"{nome_modulo}/{num.lower().replace(' ', '-')}.pdf"
            zip_file.writestr(pdf_filename, pdf_buffer.getvalue())
    
    buffer_zip.seek(0)
    st.success("🎉 Módulo gerado com ilustrações automáticas com sucesso!")
    st.download_button(
        label="📥 Baixar ZIP com o Módulo Completo",
        data=buffer_zip,
        file_name=f"{nome_modulo}.zip",
        mime="application/zip"
    )
