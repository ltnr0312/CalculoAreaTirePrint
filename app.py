import streamlit as st
import cv2
import numpy as np

# Função para processar a imagem
def process_image(image, largura_mm, altura_mm):
    # Converter a imagem para escala de cinza
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Aplicar um limiar (threshold) para binarizar a imagem
    _, binary_image = cv2.threshold(gray_image, 1, 255, cv2.THRESH_BINARY)
    
    # Calcular a área da cor grafite (pixels brancos na imagem binarizada)
    grafite_area = np.sum(binary_image == 255)
    
    # Calcular a área total da imagem
    total_area = binary_image.size
    
    # Calcular a proporção da área de cor grafite
    proportion_grafite = grafite_area / total_area
    
    # Dimensões da imagem em pixels
    largura_px = image.shape[1]
    altura_px = image.shape[0]
    
    # Resolução em pixels por milímetro
    resolucao_px_mm = (largura_px / largura_mm, altura_px / altura_mm)
    
    # Área de um pixel em milímetros quadrados
    area_pixel_mm2 = (1 / resolucao_px_mm[0]) * (1 / resolucao_px_mm[1])
    
    # Calcular a área da cor grafite em milímetros quadrados
    area_grafite_mm2 = grafite_area * area_pixel_mm2

    return binary_image, proportion_grafite, area_grafite_mm2

# Título do App
st.title('Análise de Imagem de Pneu')

# Upload da imagem
uploaded_file = st.file_uploader("Carregar imagem", type=["png", "jpg", "jpeg"])

# Input das dimensões da imagem
largura_mm = st.number_input('Largura da imagem (mm)', min_value=1.0)
altura_mm = st.number_input('Altura da imagem (mm)', min_value=1.0)

# Aviso para editar a foto
st.warning('Por favor, edite a foto com o tamanho real e em tons de cinza para facilitar a análise.')

if uploaded_file and largura_mm > 0 and altura_mm > 0:
    # Leitura da imagem
    image = cv2.imdecode(np.frombuffer(uploaded_file.read(), np.uint8), cv2.IMREAD_COLOR)
    
    if st.button('Executar'):
        # Processamento da imagem
        binary_image, proportion_grafite, area_grafite_mm2 = process_image(image, largura_mm, altura_mm)
        
        # Mostrar a imagem original e binarizada lado a lado
        col1, col2 = st.columns(2)
        with col1:
            st.image(cv2.cvtColor(image, cv2.COLOR_BGR2RGB), caption='Imagem Original', use_column_width=True)
        with col2:
            st.image(binary_image, caption='Imagem Binarizada', use_column_width=True)
        
        # Calcular a área em centímetros quadrados
        area_grafite_cm2 = area_grafite_mm2 / 100
        
        # Mostrar os resultados com vírgula como separador decimal
        st.write(f'A proporção da área de cor grafite é: {proportion_grafite * 100:.2f}%'.replace('.', ','))
        st.write(f'A área da cor grafite é aproximadamente: {area_grafite_mm2:.2f} mm²'.replace('.', ','))
        st.write(f'A área da cor grafite é aproximadamente: {area_grafite_cm2:.2f} cm²'.replace('.', ','))
