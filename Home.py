import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="Home",
    page_icon=""
)

#image_path='C:/Users/wnogueib/Repos/'
image = Image.open( 'logo.png')
st.sidebar.image(image, width=120)

st.sidebar.markdown('# Cury Companany')
st.sidebar.markdown('## Fasted Delivery in Town')
st.sidebar.markdown("""____""")

st.write(" # Cury Company Growth DashBoard")

st.markdown(
    """
    Growth Dashboard foi construído para acompanhar as métricas de crescimento dos Entregadores e Restaurantes.
    ### Como utilizar este Growth Dashboard?
    - Visão empresa:
        -Visão Gerencial: Métricas gerais de comportamento.
        -Visão Tática: Indicadores semanais de crescimento.
        -Visão Geográfica: Insights de Geolocalização.
    - Visão entregador:
        -Acompanhamento dos indicadores semanais de crescimento.
    - Visão restaurante:
        -Indicadores semanais de crescimento dos restaurantes
    ### Ask for help
    _ Time Data Science no Discord
        @willian
        
""")


    