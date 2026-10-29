import os
import zipfile
import io
import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.graphics.shapes import Drawing, Rect, Circle, Line, String, Polygon, PolyLine
from PIL import Image as PILImage, ImageDraw
from io import BytesIO

# Configuração do Streamlit
st.set_page_config(page_title="Gerador Pro - Kit EdukaKids", page_icon="🎨", layout="centered")
st.title("🎨 Painel Avançado - Kit EdukaKids Pro")
st.markdown("Sistema inteligente para geração automatizada de apostilas com múltiplos layouts pedagógicos e identidade visual oficial.")

# --- GARANTIA DE ESTRUTURA E ASSETS ---
if not os.path.exists("assets"):
    os.makedirs("assets")

# Cria uma logo padrão e imagens de exemplo se não existirem
logo_default_path = "assets/EdukakidsLogo.jpg"
if not os.path.exists(logo_default_path):
    img_logo = PILImage.new("RGB", (200, 200), "#1d3557")
    d_logo = ImageDraw.Draw(img_logo)
    d_logo.rectangle([10, 10, 190, 190], outline="white", width=4)
    d_logo.text((45, 90), "EdukaKids", fill="white")
    img_logo.save(logo_default_path)

# Cria imagens de exemplo na pasta assets se estiver vazia
imagens_exemplo = {"urso.png": "Urso", "maca.png": "Maca", "estrela.png": "Estrela", "casa.png": "Casa"}
for img_nome, img_texto in imagens_exemplo.items():
    caminho_i = os.path.join("assets", img_nome)
    if not os.path.exists(caminho_i):
        im = PILImage.new("RGB", (300, 300), "white")
        draw_im = ImageDraw.Draw(im)
        draw_im.rectangle([15, 15, 285, 285], outline="black", width=3)
        draw_im.text((90, 140), img_texto, fill="black")
        im.save(caminho_i)

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
    "Atividade de Contagem e Matemática",
    "Atividade de Pintura e Formas Livres"
]

# --- FUNÇÃO DE GERAÇÃO GRÁFICA (Definida antes de ser chamada) ---
def gerar_grafico_por_layout(layout_tipo):
    """Gera o motor gráfico vetorial adequado para cada tipo de atividade pedagógica"""
    d = Drawing(500, 300)

    # Moldura padrão profissional da ficha
    d.add(Rect(10, 10, 480, 280, rx=10, ry=10, fillColor=colors.white, strokeColor=colors.HexColor('#1d3557'), strokeWidth=2))

    if "Caligrafia" in layout_tipo:
        d.add(String(150, 255, "• TREINANDO A ESCRITA E O TRAÇADO •", fontSize=11, fillColor=colors.HexColor('#1d3557'), fontName="Helvetica-Bold"))
        for y_pos in [190, 120, 50]:
            d.add(Line(30, y_pos + 30, 470, y_pos + 30, strokeColor=colors.HexColor('#ced4da'), strokeWidth=1))
            d.add(Line(30, y_pos + 15, 470, y_pos + 15, strokeColor=colors.HexColor('#457b9d'), strokeWidth=1.5, strokeDashArray=[4, 4]))
            d.add(Line(30, y_pos, 470, y_pos, strokeColor=colors.HexColor('#ced4da'), strokeWidth=1))
            d.add(String(50, y_pos + 5, "A a   B b   C c   D d   E e", fontSize=18, fillColor=colors.HexColor('#adb5bd'), fontName="Helvetica-Bold"))

    elif "Ligar os Pontos" in layout_tipo:
        d.add(String(150, 255, "• LIGUE OS PONTOS NA ORDEM NUMÉRICA •", fontSize=11, fillColor=colors.HexColor('#1d3557'), fontName="Helvetica-Bold"))
        coords = [(200, 200, "1"), (250, 230, "2"), (310, 220, "3"), (340, 160, "4"), (290, 100, "5"), (220, 100, "6"), (170, 150, "7")]
        for px, py, pnum in coords:
            d.add(Circle(px, py, 5, fillColor=colors.HexColor('#1d3557'), strokeColor=colors.HexColor('#1d3557')))
            d.add(Circle(px, py, 12, fillColor=colors.white, strokeColor=colors.HexColor('#e63946'), strokeWidth=1, strokeDashArray=[2, 2]))
            d.add(String(px - 3, py - 4, pnum, fontSize=9, fillColor=colors.HexColor('#e63946'), fontName="Helvetica-Bold"))

    elif "Labirinto" in layout_tipo:
        d.add(String(160, 255, "• ENCONTRE A SAÍDA DO LABIRINTO •", fontSize=11, fillColor=colors.HexColor('#1d3557'), fontName="Helvetica-Bold"))
        d.add(Rect(60, 40, 380, 200, rx=5, ry=5, fillColor=colors.white, strokeColor=colors.HexColor('#1d3557'), strokeWidth=2))
        d.add(Rect(100, 70, 80, 120, rx=5, ry=5, fillColor=colors.HexColor('#f1faee'), strokeColor=colors.HexColor('#457b9d'), strokeWidth=1.5))
        d.add(Rect(220, 90, 180, 80, rx=5, ry=5, fillColor=colors.HexColor('#f1faee'), strokeColor=colors.HexColor('#457b9d'), strokeWidth=1.5))
        d.add(String(75, 50, "INÍCIO", fontSize=9, fontName="Helvetica-Bold", fillColor=colors.HexColor('#e63946')))
        d.add(String(390, 210, "FIM", fontSize=9, fontName="Helvetica-Bold", fillColor=colors.HexColor('#2a9d8f')))

    elif "Cruzadinha" in layout_tipo:
        d.add(String(160, 255, "• CAÇA-PALAVRAS E CRUZADINHA •", fontSize=11, fillColor=colors.HexColor('#1d3557'), fontName="Helvetica-Bold"))
        for r in range(4):
            for c in range(8):
                d.add(Rect(90 + (c * 40), 60 + (r * 35), 32, 32, fillColor=colors.white, strokeColor=colors.HexColor('#1d3557'), strokeWidth=1))
        d.add(String(100, 215, "A   B   C   D   E   F   G   H", fontSize=11, fontName="Helvetica-Bold", fillColor=colors.HexColor('#457b9d')))

    elif "Contagem" in layout_tipo:
        d.add(String(165, 255, "• CONTE OS ELEMENTOS E REGISTRE •", fontSize=11, fillColor=colors.HexColor('#1d3557'), fontName="Helvetica-Bold"))
        # Desenha itens repetidos para contagem visual
        for i in range(5):
            cx = 70 + (i * 75)
            d.add(Circle(cx, 140, 22, fillColor=colors.HexColor('#a8dadc'), strokeColor=colors.HexColor('#1d3557'), strokeWidth=1.5))
            d.add(String(cx - 4, d.height/2 - 3, str(i+1), fontSize=12, fontName="Helvetica-Bold", fillColor=colors.HexColor('#1d3557')))
        d.add(Rect(150, 45, 200, 35, rx=5, ry=5, fillColor=colors.white, strokeColor=colors.HexColor('#457b9d'), strokeWidth=1.5))
        d.add(String(165, 55, "Total de elementos: _________", fontSize=10, fontName="Helvetica-Bold", fillColor=colors.HexColor('#1d3557')))

    else:
        d.add(String(165, 255, "• ESPAÇO DE CRIAÇÃO E PINTURA •", fontSize=11, fillColor=colors.HexColor('#1d3557'), fontName="Helvetica-Bold"))
        d.add(Rect(40, 30, 420, 210, rx=10, ry=10, fillColor=colors.HexColor('#f8f9fa'), strokeColor=colors.HexColor('#457b9d'), strokeWidth=1.5, strokeDashArray=[5, 5]))
        d.add(String(170, 130, "🎨 Desenhe ou Pinte aqui", fontSize=12, fontName="Helvetica-Bold", fillColor=colors.HexColor('#6c757d')))

    return d

# --- INTERFACE PRINCIPAL ---
st.subheader("📝 Editor de Fichas e Layouts Pedagógicos")
fichas_data = []
previews = []

arquivos_assets = [f for f in os.listdir("assets") if f.lower().endswith(('png', 'jpg', 'jpeg'))] if os.path.exists("assets") else []

for i in range(1, int(quantidade) + 1):
    with st.expander(f"Ficha {i:02d}", expanded=(i == 1)):
        col1, col2, col3 = st.columns([1, 1.5, 1.5])
        with col1:
            num = st.text_input(f"ID #{i}", value=f"Ficha {i:02d}", key=f"num_{i}")
        with col2:
            titulo = st.text_input(f"Título #{i}", value=f"Atividade Divertida {i}", key=f"titulo_{i}")
        with col3:
            layout_escolhido = st.selectbox(f"Layout #{i}", tipos_layout_opcoes, key=f"layout_{i}")
            imagem = st.selectbox(f"Imagem #{i}", [""] + arquivos_assets, key=f"imagem_{i}")

        instrucao = st.text_area(f"Instrução / Enunciado #{i}", value=f"Siga as orientações da atividade {i} com bastante atenção e capricho.", key=f"instr_{i}")

        # Botão de Pré-visualização individual
        if st.button(f"🔍 Pré-visualizar {i:02d}", key=f"preview_{i}"):
            pdf_buffer = BytesIO()
            doc = SimpleDocTemplate(pdf_buffer, pagesize=A4, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
            story = []

            logo_path = "assets/EdukakidsLogo.jpg"
            logo_img = Image(logo_path, width=50, height=50) if os.path.exists(logo_path) else Paragraph("<b>EdukaKids</b>", getSampleStyleSheet()['Normal'])

            header_data = [
                [logo_img, Paragraph("<b>ESCOLA:</b> __________________________________________________<br/><br/><b>ALUNO(A):</b> _________________________________ <b>DATA:</b> ___/___/_____", getSampleStyleSheet()['Normal'])]
            ]
            header_table = Table(header_data, colWidths=[70, 430])
            header_table.setStyle(TableStyle([
                ('BOX', (0, 0), (-1, -1), 1.5, colors.HexColor('#1d3557')),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('PADDING', (0, 0), (-1, -1), 4),
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f8f9fa'))
            ]))

            story.append(header_table)
            story.append(Spacer(1, 8))

            styles = getSampleStyleSheet()
            title_style = ParagraphStyle('TitleStyle', parent=styles['Heading1'], fontSize=13, textColor=colors.HexColor('#1d3557'), alignment=1, spaceAfter=3)
            body_style = ParagraphStyle('BodyStyle', parent=styles['Normal'], fontSize=10, textColor=colors.HexColor('#457b9d'), alignment=1, spaceAfter=8)

            story.append(Paragraph(f"<b>{num}: {titulo}</b>", title_style))
            story.append(Paragraph(instrucao, body_style))

            # Se houver imagem selecionada, insere no fluxo fora do Drawing para evitar conflitos
            if imagem:
                caminho_img_sel = os.path.join("assets", imagem)
                if os.path.exists(caminho_img_sel):
                    story.append(Image(caminho_img_sel, width=120, height=120))
                    story.append(Spacer(1, 5))

            story.append(gerar_grafico_por_layout(layout_escolhido))

            doc.build(story)
            pdf_buffer.seek(0)

            # Conversão segura para exibição no Streamlit
            try:
                from pdf2image import convert_from_bytes
                imagens_pdf = convert_from_bytes(pdf_buffer.getvalue())
                if imagens_pdf:
                    previews.append((i, imagens_pdf[0]))
            except Exception:
                st.info("💡 PDF gerado com sucesso! (Instale a biblioteca pdf2image se quiser visualizar o print direto na tela)")

        fichas_data.append((num, titulo, instrucao, layout_escolhido, imagem))

# Exibir pré-visualizações geradas
if previews:
    st.subheader("👀 Pré-visualização das Fichas")
    for i, pil_image in previews:
        st.image(pil_image, caption=f"Ficha {i:02d} - Pré-visualização", use_container_width=True)

# --- BOTÃO DE GERAÇÃO DO PACOTE COMPLETO EM ZIP ---
if st.button("🚀 Gerar Pacote Profissional em ZIP", type="primary"):
    buffer_zip = BytesIO()

    with zipfile.ZipFile(buffer_zip, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for num, titulo, instrucao, layout_escolhido, imagem in fichas_data:
            pdf_buffer = BytesIO()

            doc = SimpleDocTemplate(pdf_buffer, pagesize=A4, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
            story = []

            logo_path = "assets/EdukakidsLogo.jpg"
            logo_img = Image(logo_path, width=50, height=50) if os.path.exists(logo_path) else Paragraph("<b>EdukaKids</b>", getSampleStyleSheet()['Normal'])

            header_data = [
                [logo_img, Paragraph("<b>ESCOLA:</b> __________________________________________________<br/><br/><b>ALUNO(A):</b> _________________________________ <b>DATA:</b> ___/___/_____", getSampleStyleSheet()['Normal'])]
            ]
            header_table = Table(header_data, colWidths=[70, 430])
            header_table.setStyle(TableStyle([
                ('BOX', (0, 0), (-1, -1), 1.5, colors.HexColor('#1d3557')),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('PADDING', (0, 0), (-1, -1), 4),
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f8f9fa'))
            ]))

            story.append(header_table)
            story.append(Spacer(1, 8))

            styles = getSampleStyleSheet()
            title_style = ParagraphStyle('TitleStyle', parent=styles['Heading1'], fontSize=13, textColor=colors.HexColor('#1d3557'), alignment=1, spaceAfter=3)
            body_style = ParagraphStyle('BodyStyle', parent=styles['Normal'], fontSize=10, textColor=colors.HexColor('#457b9d'), alignment=1, spaceAfter=8)

            story.append(Paragraph(f"<b>{num}: {titulo}</b>", title_style))
            story.append(Paragraph(instrucao, body_style))

            if imagem:
                caminho_img_sel = os.path.join("assets", imagem)
                if os.path.exists(caminho_img_sel):
                    story.append(Image(caminho_img_sel, width=120, height=120))
                    story.append(Spacer(1, 5))

            story.append(gerar_grafico_por_layout(layout_escolhido))

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

# Botão para limpar dados
if st.button("🔄 Recarregar / Limpar Estado", type="secondary"):
    st.rerun()
