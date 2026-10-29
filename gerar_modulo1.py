import os
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# Lista completa das 20 fichas do Módulo 1
fichas = [
    ("Ficha 01", "A é para Abrigo", "Encontre a letra A no abrigo e cubra o caminho até ela."),
    ("Ficha 02", "E é para Elefante", "Ajude o elefante a encher o rino com a letra E."),
    ("Ficha 03", "I é para Iglu", "Toque o iglu com a letra I."),
    ("Ficha 04", "O é para Oceano", "Trace o caminho do peixe com a letra O."),
    ("Ficha 05", "U é para Urso", "Encontre a letra U no urso e complete a forminha."),
    ("Ficha 06", "B é para Bola", "Bater a bola com a letra B."),
    ("Ficha 07", "C é para Cavalo", "Cavalgar o cavalo com a letra C."),
    ("Ficha 08", "D é para Dinossauro", "Dizer o nome do dinossauro com a letra D."),
    ("Ficha 09", "F é para Foguete", "Pintar o foguete com a letra F."),
    ("Ficha 10", "G é para Girafa", "Contar o pescoço da girafa com a letra G."),
    ("Ficha 11", "H é para Hipopótamo", "Encenar o hipopótamo com a letra H."),
    ("Ficha 12", "J é para Jardim", "Caminhar no jardim com a letra J."),
    ("Ficha 13", "K é para Kiwi", "Descobrir o kiwi com a letra K."),
    ("Ficha 14", "L é para Leão", "Rugir como leão com a letra L."),
    ("Ficha 15", "M é para Macaco", "Pular como macaco com a letra M."),
    ("Ficha 16", "N é para Nave", "Contar estrelas na nave com a letra N."),
    ("Ficha 17", "P é para Pato", "Nadar como pato com a letra P."),
    ("Ficha 18", "Q é para Queijo", "Derreter o queijo com a letra Q."),
    ("Ficha 19", "R é para Ratinho", "Correr como ratinho com a letra R."),
    ("Ficha 20", "S é para Sapo", "Pular como sapo com a letra S.")
]

pasta_destino = "01-Alfabetizacao-Divertida"
os.makedirs(pasta_destino, exist_ok=True)

styles = getSampleStyleSheet()
title_style = ParagraphStyle(
    'TitleStyle',
    parent=styles['Heading1'],
    fontSize=18,
    textColor=colors.HexColor('#1d3557'),
    alignment=1,
    spaceAfter=15
)
body_style = ParagraphStyle(
    'BodyStyle',
    parent=styles['Normal'],
    fontSize=12,
    textColor=colors.HexColor('#457b9d'),
    alignment=1,
    spaceAfter=30
)
info_style = ParagraphStyle(
    'InfoStyle',
    parent=styles['Normal'],
    fontSize=10,
    textColor=colors.black,
    alignment=0
)

for num, titulo, instrucao in fichas:
    nome_arquivo = os.path.join(pasta_destino, f"{num.lower().replace(' ', '-')}.pdf")
    doc = SimpleDocTemplate(nome_arquivo, pagesize=A4, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    story = []
    
    if os.path.exists("EdukakidsLogo.jpg"):
        story.append(Image("EdukakidsLogo.jpg", width=90, height=90))
        story.append(Spacer(1, 10))
        
    story.append(Paragraph("<b>Nome:</b> ____________________________________ &nbsp;&nbsp;&nbsp;&nbsp; <b>Data:</b> ___/___/______", info_style))
    story.append(Spacer(1, 30))
    
    story.append(Paragraph(f"<b>{num}: {titulo}</b>", title_style))
    story.append(Paragraph(instrucao, body_style))
    
    doc.build(story)

print("Todas as 20 fichas do Módulo 1 foram geradas automaticamente com sucesso!")