import os
import zipfile
import io
import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.graphics.shapes import Drawing, Rect, Circle, Line, String, Polygon
from PIL import Image as PILImage
from io import BytesIO

# Configuração do Streamlit
st.set_page_config(page_title="Gerador Pro - Kit EdukaKids", page_icon="🎨", layout="centered")
st.title("🎨 Painel Avançado - Kit EdukaKids Pro")
st.markdown("Sistema inteligente para geração automatizada de apostilas com múltiplos layouts pedagógicos e identidade visual oficial.")

# Configurações na Barra Lateral
st.sidebar.header("📁 Configurações do Módulo")
nome_modulo = st.sidebar.text_input("Nome da Pasta do Módulo", "01-Alfabetizacao-Divertida")
quantidade = st.sidebar.slider("Número de Fichas do Lote", min_value=1, max_value=30, value=6)

# Tipos de Layouts disponíveis
tipos_layout_opcoes = [
    "Caligrafia Escolar (Pautas e Pontilhados)",
    "Ligar os Pontos (Numeração Sequencial)",
    "Labirinto / Circuito de Traçado",
    "Cruzadinha / Caça-Palavras (Estruturado)",
    "Atividade de Pintura e Formas Livres"
]

# Dados das Fichas
st.subheader("📝 Editor de Fichas e Layouts Pedagógicos")
fichas_data = []
previews = []

for i in range(1, int(quantidade) + 1):
    with st.expander(f"Ficha {i:02d}", expanded=(i == 1)):
        col1, col2, col3 = st.columns([1, 1.5, 1.5])
        with col1:
            num = st.text_input(f"ID #{i}", value=f"Ficha {i:02d}", key=f"num_{i}")
        with col2:
            titulo = st.text_input(f"Título #{i}", value=f"Atividade Divertida {i}", key=f"titulo_{i}")
        with col3:
            layout_escolhido = st.selectbox(f"Layout #{i}", tipos_layout_opcoes, key=f"layout_{i}")
            imagem = st.selectbox(f"Imagem #{i}", [""] + os.listdir("assets/"), key=f"imagem_{i}")

        instrucao = st.text_area(f"Instrução / Enunciado #{i}", value=f"Siga as orientações da atividade {i} com bastante atenção e capricho.", key=f"instr_{i}")

        # Botão para atualizar a pré-visualização
        if st.button(f"🔍 Pré-visualizar {i:02d}", key=f"preview_{i}"):
            pdf_buffer = BytesIO()
            doc = SimpleDocTemplate(pdf_buffer, pagesize=A4, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
            story = []

            # Cabeçalho Comercial com Logo Oficial
            logo_path = "assets/EdukakidsLogo.jpg"
            logo_img = Image(logo_path, width=60, height=60) if os.path.exists(logo_path) else Paragraph("<b>EdukaKids</b>", getSampleStyleSheet()['Normal'])

            header_data = [
                [logo_img, Paragraph("<b>ESCOLA:</b> __________________________________________________<br/><br/><b>ALUNO(A):</b> _________________________________ <b>DATA:</b> ___/___/_____", getSampleStyleSheet()['Normal'])]
            ]
            header_table = Table(header_data, colWidths=[75, 425])
            header_table.setStyle(TableStyle([
                ('BOX', (0, 0), (-1, -1), 1.5, colors.HexColor('#1d3557')),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('PADDING', (0, 0), (-1, -1), 5),
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f8f9fa'))
            ]))

            story.append(header_table)
            story.append(Spacer(1, 10))

            styles = getSampleStyleSheet()
            title_style = ParagraphStyle('TitleStyle', parent=styles['Heading1'], fontSize=14, textColor=colors.HexColor('#1d3557'), alignment=1, spaceAfter=4)
            body_style = ParagraphStyle('BodyStyle', parent=styles['Normal'], fontSize=10, textColor=colors.HexColor('#457b9d'), alignment=1, spaceAfter=10)

            story.append(Paragraph(f"<b>{num}: {titulo}</b>", title_style))
            story.append(Paragraph(instrucao, body_style))

            # Insere o layout gráfico dinâmico escolhido para esta ficha
            story.append(gerar_grafico_por_layout(layout_escolhido, image_path=f"assets/{imagem}" if imagem else None))

            doc.build(story)
            pdf_buffer.seek(0)

            # Convert PDF to an image
            pil_image = PILImage.open(BytesIO(pdf_buffer.getvalue()))
            previews.append((i, pil_image))

        fichas_data.append((num, titulo, instrucao, layout_escolhido, imagem))

# Função para gerar o layout gráfico
def gerar_grafico_por_layout(layout_tipo, image_path=None):
    """Gera o motor gráfico vetorial adequado para cada tipo de atividade pedagógica"""
    d = Drawing(500, 340)

    # Moldura padrão profissional da ficha
    d.add(Rect(10, 10, 480, 320, rx=10, ry=10, fillColor=colors.white, strokeColor=colors.HexColor('#1d3557'), strokeWidth=2))

    if "Caligrafia" in layout_tipo:
        d.add(String(160, 290, "• TREINANDO A ESCRITA E TRAÇADO •", fontSize=11, fillColor=colors.HexColor('#1d3557'), fontName="Helvetica-Bold"))
        for y_pos in [220, 140, 60]:
            d.add(Line(30, y_pos + 35, 470, y_pos + 35, strokeColor=colors.HexColor('#ced4da'), strokeWidth=1))
            d.add(Line(30, y_pos + 20, 470, y_pos + 20, strokeColor=colors.HexColor('#457b9d'), strokeWidth=1.5, strokeDashArray=[4, 4]))
            d.add(Line(30, y_pos, 470, y_pos, strokeColor=colors.HexColor('#ced4da'), strokeWidth=1))
            d.add(String(50, y_pos + 8, "A a  B b  C c  D d  E e", fontSize=20, fillColor=colors.HexColor('#adb5bd'), fontName="Helvetica-Bold"))

    elif "Ligar os Pontos" in layout_tipo:
        d.add(String(170, 290, "• LIGUE OS PONTOS NA ORDEM NUMÉRICA •", fontSize=11, fillColor=colors.HexColor('#1d3557'), fontName="Helvetica-Bold"))
        coords = [(220, 220, "1"), (270, 250, "2"), (330, 240, "3"), (360, 180, "4"), (320, 120, "5"), (250, 110, "6"), (200, 160, "7")]
        for px, py, pnum in coords:
            d.add(Circle(px, py, 6, fillColor=colors.HexColor('#1d3557'), strokeColor=colors.HexColor('#1d3557')))
            d.add(Circle(px, py, 14, fillColor=colors.white, strokeColor=colors.HexColor('#e63946'), strokeWidth=1, strokeDashArray=[2, 2]))
            d.add(String(px - 3, py - 4, pnum, fontSize=9, fillColor=colors.HexColor('#e63946'), fontName="Helvetica-Bold"))

    elif "Labirinto" in layout_tipo:
        d.add(String(180, 290, "• ENCONTRE A SAÍDA DO LABIRINTO •", fontSize=11, fillColor=colors.HexColor('#1d3557'), fontName="Helvetica-Bold"))
        d.add(Rect(60, 60, 380, 200, rx=5, ry=5, fillColor=colors.white, strokeColor=colors.HexColor('#1d3557'), strokeWidth=2))
        d.add(Rect(100, 100, 80, 120, rx=5, ry=5, fillColor=colors.HexColor('#f1faee'), strokeColor=colors.HexColor('#457b9d'), strokeWidth=1.5))
        d.add(Rect(220, 120, 180, 80, rx=5, ry=5, fillColor=colors.HexColor('#f1faee'), strokeColor=colors.HexColor('#457b9d'), strokeWidth=1.5))
        d.add(String(75, 75, "INÍCIO", fontSize=9, fontName="Helvetica-Bold", fillColor=colors.HexColor('#e63946')))
        d.add(String(400, 230, "FIM", fontSize=9, fontName="Helvetica-Bold", fillColor=colors.HexColor('#2a9d8f')))

    elif "Cruzadinha" in layout_tipo:
        d.add(String(170, 290, "• CAÇA-PALAVRAS E CRUZADINHA •", fontSize=11, fillColor=colors.HexColor('#1d3557'), fontName="Helvetica-Bold"))
        for r in range(4):
            for c in range(8):
                d.add(Rect(90 + (c * 40), 90 + (r * 40), 35, 35, fillColor=colors.white, strokeColor=colors.HexColor('#1d3557'), strokeWidth=1))
        d.add(String(100, 255, "A   B   C   D   E   F   G   H", fontSize=12, fontName="Helvetica-Bold", fillColor=colors.HexColor('#457b9d')))

    else:
        d.add(String(170, 290, "• ESPAÇO DE CRIAÇÃO E PINTURA •", fontSize=11, fillColor=colors.HexColor('#1d3557'), fontName="Helvetica-Bold"))
        d.add(Rect(50, 50, 400, 210, rx=15, ry=15, fillColor=colors.HexColor('#f8f9fa'), strokeColor=colors.HexColor('#457b9d'), strokeWidth=1.5, strokeDashArray=[6, 6]))
        d.add(String(165, 145, "🎨 Cole ou Desenhe aqui", fontSize=14, fontName="Helvetica-Bold", fillColor=colors.HexColor('#6c757d')))
        if image_path and os.path.exists(image_path):
            image = Image(image_path, width=400, height=200)
            d.add(image)

    return d

# Exibir pré-visualizações
if previews:
    st.subheader("👀 Pré-visualização das Fichas")
    for i, pil_image in previews:
        st.image(pil_image, caption=f"Ficha {i:02d} - Pré-visualização", use_column_width=True)

# Botão para gerar o pacote profissional
if st.button("🚀 Gerar Pacote Profissional em ZIP", type="primary"):
    buffer_zip = BytesIO()

    with zipfile.ZipFile(buffer_zip, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for num, titulo, instrucao, layout_escolhido, imagem in fichas_data:
            pdf_buffer = BytesIO()

            doc = SimpleDocTemplate(pdf_buffer, pagesize=A4, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
            story = []

            # Cabeçalho Comercial com Logo Oficial
            logo_path = "assets/EdukakidsLogo.jpg"
            logo_img = Image(logo_path, width=60, height=60) if os.path.exists(logo_path) else Paragraph("<b>EdukaKids</b>", getSampleStyleSheet()['Normal'])

            header_data = [
                [logo_img, Paragraph("<b>ESCOLA:</b> __________________________________________________<br/><br/><b>ALUNO(A):</b> _________________________________ <b>DATA:</b> ___/___/_____", getSampleStyleSheet()['Normal'])]
            ]
            header_table = Table(header_data, colWidths=[75, 425])
            header_table.setStyle(TableStyle([
                ('BOX', (0, 0), (-1, -1), 1.5, colors.HexColor('#1d3557')),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('PADDING', (0, 0), (-1, -1), 5),
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f8f9fa'))
            ]))

            story.append(header_table)
            story.append(Spacer(1, 10))

            styles = getSampleStyleSheet()
            title_style = ParagraphStyle('TitleStyle', parent=styles['Heading1'], fontSize=14, textColor=colors.HexColor('#1d3557'), alignment=1, spaceAfter=4)
            body_style = ParagraphStyle('BodyStyle', parent=styles['Normal'], fontSize=10, textColor=colors.HexColor('#457b9d'), alignment=1, spaceAfter=10)

            story.append(Paragraph(f"<b>{num}: {titulo}</b>", title_style))
            story.append(Paragraph(instrucao, body_style))

            # Insere o layout gráfico dinâmico escolhido para esta ficha
            story.append(gerar_grafico_por_layout(layout_escolhido, image_path=f"assets/{imagem}" if imagem else None))

            doc.build(story)

            pdf_filename = f"{nome_modulo}/{num.lower().replace(' ', '-')}.pdf"
            zip_file.writestr(pdf_filename, pdf_buffer.getvalue())

    buffer_zip.seek(0)
    st.success("🎉 Apostila gerada com sucesso com múltiplos layouts profissionais!")
    st.download_button(
        label="📥 Baixar ZIP com o Módulo Completo",
        data=buffer_zip,
        file_name=f"{nome_modulo}.zip",
        mime="application/zip"
    )

# Limpar os dados
if st.button(" #=> Limpar Dados", type="secondary"):
    fichas_data = []
    previews = []
    st.experimental_rerun()
