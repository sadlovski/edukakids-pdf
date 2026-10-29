import os
import zipfile
import io
import math
import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.graphics.shapes import Drawing, Rect, Circle, Line, String, Polygon, PolyLine

st.set_page_config(page_title="Gerador Kit EdukaKids Pro", page_icon="🎨", layout="centered")

st.title("🎨 Gerador Profissional - Kit EdukaKids")
st.markdown("Painel de alta performance para criação de apostilas infantis com múltiplos layouts (Ligar Pontos, Caligrafia e Atividades).")

# Barra Lateral
st.sidebar.header("📁 Configurações do Módulo")
nome_modulo = st.sidebar.text_input("Nome da Pasta do Módulo", "01-Alfabetizacao-Divertida")
quantidade = st.sidebar.slider("Número de Fichas", min_value=1, max_value=30, value=6)

st.subheader("📝 Conteúdo das Fichas")

fichas_data = []
for i in range(1, int(quantidade) + 1):
    with st.expander(f"Ficha {i:02d}", expanded=(i == 1)):
        col1, col2 = st.columns([1, 2])
        with col1:
            num = st.text_input(f"Identificador #{i}", value=f"Ficha {i:02d}", key=f"num_{i}")
        with col2:
            titulo = st.text_input(f"Título #{i}", value=f"Atividade Divertida {i}", key=f"titulo_{i}")
        instrucao = st.text_area(f"Instrução da Ficha #{i}", value=f"Siga as orientações da atividade {i} com atenção.", key=f"instr_{i}")
        fichas_data.append((num, titulo, instrucao))

def criar_layout_atividade(titulo):
    """Gera layouts profissionais diferenciados (Ligar pontos, Caligrafia, Labirinto ou Traçado)"""
    d = Drawing(500, 360)
    
    # Moldura principal da atividade (estilo ficha comercial)
    d.add(Rect(10, 10, 480, 340, rx=10, ry=10, fillColor=colors.white, strokeColor=colors.HexColor('#2b2d42'), strokeWidth=2))
    
    t_lower = titulo.lower()
    
    if "ponto" in t_lower or "ligar" in t_lower or "22" in t_lower:
        # Layout de Ligar os Pontos com numeração em formato de estrela/casinha
        d.add(String(200, 320, "• LIGUE OS PONTOS NA ORDEM •", fontSize=12, fillColor=colors.HexColor('#2b2d42'), fontName="Helvetica-Bold"))
        
        # Coordenadas formando uma estrela/desenho geométrico numerado
        pontos = [
            (250, 260, "1"), (280, 210, "2"), (340, 210, "3"), 
            (290, 170, "4"), (310, 110, "5"), (250, 140, "6"), 
            (190, 110, "7"), (210, 170, "8"), (160, 210, "9"), (220, 210, "10")
        ]
        
        for px, py, pnum in pontos:
            d.add(Circle(px, py, 6, fillColor=colors.HexColor('#2b2d42'), strokeColor=colors.HexColor('#2b2d42')))
            d.add(Circle(px, py, 14, fillColor=colors.white, strokeColor=colors.HexColor('#8d99ae'), strokeWidth=1, strokeDashArray=[2, 2]))
            d.add(String(px - 4, py - 4, pnum, fontSize=9, fillColor=colors.HexColor('#d90429'), fontName="Helvetica-Bold"))
            
    elif "caligrafia" in t_lower or "letra" in t_lower or "vogal" in t_lower or "família" in t_lower:
        # Layout de Caligrafia Escolar (Linhas pautadas duplas/triplas)
        d.add(String(30, 320, "• TREINANDO A ESCRITA •", fontSize=12, fillColor=colors.HexColor('#2b2d42'), fontName="Helvetica-Bold"))
        
        for linha_y in [250, 170, 90]:
            # Linha guia caligráfica
            d.add(Line(40, linha_y + 30, 460, linha_y + 30, strokeColor=colors.HexColor('#adb5bd'), strokeWidth=1))
            d.add(Line(40, linha_y + 15, 460, linha_y + 15, strokeColor=colors.HexColor('#457b9d'), strokeWidth=1.5, strokeDashArray=[4, 4]))
            d.add(Line(40, linha_y, 460, linha_y, strokeColor=colors.HexColor('#adb5bd'], strokeWidth=1))
            
            # Exemplo pontilhado para caligrafia
            d.add(String(60, linha_y + 8, "A a A a A a A a A a", fontSize=22, fillColor=colors.HexColor('#ced4da'), fontName="Helvetica-Bold"))
            
    else:
        # Layout de Traçado e Circuito Divertido
        d.add(String(180, 320, "• TRACE O CAMINHO CORRETO •", fontSize=12, fillColor=colors.HexColor('#2b2d42'), fontName="Helvetica-Bold"))
        
        # Pista em zigue-zague pontilhada
        path_points = [(50, 180), (150, 250), (250, 110), (350, 250), (450, 180)]
        for i in range(len(path_points)-1):
            p1 = path_points[i]
            p2 = path_points[i+1]
            d.add(Line(p1[0], p1[1], p2[0], p2[1], strokeColor=colors.HexColor('#2b2d42'), strokeWidth=3, strokeDashArray=[6, 6]))
            
        # Ícones de início e fim
        d.add(Circle(50, 180, 20, fillColor=colors.white, strokeColor=colors.HexColor('#2b2d42'), strokeWidth=2))
        d.add(String(42, 175, "INÍCIO", fontSize=7, fontName="Helvetica-Bold"))
        
        d.add(Circle(450, 180, 20, fillColor=colors.white, strokeColor=colors.HexColor('#2b2d42'), strokeWidth=2))
        d.add(String(442, 175, "FIM", fontSize=8, fontName="Helvetica-Bold"))

    return d

if st.button("🚀 Gerar e Baixar Apostila Profissional em ZIP", type="primary"):
    buffer_zip = io.BytesIO()
    
    with zipfile.ZipFile(buffer_zip, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for num, titulo, instrucao in fichas_data:
            pdf_buffer = io.BytesIO()
            
            doc = SimpleDocTemplate(pdf_buffer, pagesize=A4, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
            story = []
            
            # Cabeçalho Profissional com Logo e Bloco de Identificação (Escola/Nome/Data)
            logo_path = "EdukakidsLogo.jpg"
            logo_img = Image(logo_path, width=65, height=65) if os.path.exists(logo_path) else Paragraph("<b>EdukaKids</b>", getSampleStyleSheet()['Normal'])
            
            header_data = [
                [logo_img, Paragraph("<b>ESCOLA:</b> __________________________________________________<br/><br/><b>ALUNO(A):</b> _________________________________ <b>DATA:</b> ___/___/_____", getSampleStyleSheet()['Normal'])]
            ]
            header_table = Table(header_data, colWidths=[80, 420])
            header_table.setStyle(TableStyle([
                ('BOX', (0, 0), (-1, -1), 1.5, colors.HexColor('#1d3557')),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('PADDING', (0, 0), (-1, -1), 6),
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f8f9fa'))
            ]))
            
            story.append(header_table)
            story.append(Spacer(1, 15))
            
            styles = getSampleStyleSheet()
            title_style = ParagraphStyle('TitleStyle', parent=styles['Heading1'], fontSize=15, textColor=colors.HexColor('#1d3557'), alignment=1, spaceAfter=6)
            body_style = ParagraphStyle('BodyStyle', parent=styles['Normal'], fontSize=11, textColor=colors.HexColor('#457b9d'), alignment=1, spaceAfter=12)
            
            # Título e Instrução da Atividade
            story.append(Paragraph(f"<b>{num}: {titulo}</b>", title_style))
            story.append(Paragraph(instrucao, body_style))
            
            # Adiciona o layout gráfico inteligente correspondente
            story.append(criar_layout_atividade(titulo))
            
            doc.build(story)
            
            pdf_filename = f"{nome_modulo}/{num.lower().replace(' ', '-')}.pdf"
            zip_file.writestr(pdf_filename, pdf_buffer.getvalue())
    
    buffer_zip.seek(0)
    st.success("🎉 Apostila gerada com layout profissional de alto nível!")
    st.download_button(
        label="📥 Baixar ZIP com o Kit Completo",
        data=buffer_zip,
        file_name=f"{nome_modulo}.zip",
        mime="application/zip"
    )
