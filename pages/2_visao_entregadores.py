#libraries

#para usar no terminal-----------------------------------------------------------

#alteração do endereço: cd C:\Users\wnogueib\Documents\WILLIAN\ComunidadeDS\repos\programacao_python
#  streamlit run visao_empresa.py

#================================================================================

#pip install haversine

#pip install streamlit


import haversine
from haversine import haversine

#biblioteczs

import folium
import pandas as pd
import datetime as dt
import plotly.express as px
import streamlit as st
from PIL import Image
from streamlit_folium import folium_static
#import plotly.express.object as go

st.set_page_config( page_title='Visão Entregadores', page_icon='', layout='wide')

#===================================================================
#                        Bloco de Funções
#=====================================================================
def top_entregadores(df1, top_asc):
            
    df2 = (df1.loc[:,['Time_taken(min)','City','Delivery_person_ID']]
            .groupby(['City','Delivery_person_ID']).max()
            .sort_values(['Time_taken(min)','City'], ascending = top_asc ).reset_index())

    #fazer com que apareceça somente os 10 primeiro de cada cidade

    df_aux1 = df2.loc[df2['City'] == 'Metropolitian',:].head(10)
    df_aux2 = df2.loc[df2['City'] == 'Urban',:].head(10)
    df_aux3 = df2.loc[df2['City'] == 'Semi-Urban',:].head(10)

    df3 = pd.concat([df_aux1, df_aux2, df_aux3]).reset_index()
    return df3

def clean_code(df1):
    """esta função tem a responsabilidade de limpar o dataframe
        Tipos de limpeza:
        1. Remoção dos "Na"
        2. Mudança do tipo de coluna
        3. Remoção dos espaços das variáveis
        4. Formatação da coluna de datas
        5. Limpeza da coluna tempo (remoção do texto das variaveis numericas)
        
        imput: dataframe
        output:dataframe
    """   
    linha_selecionar = df1['Delivery_person_Age'] != 'NaN ' #não seleciona linha incompativel 'Nan'
    df1 = df1.loc[linha_selecionar, :].copy()
    df1['Delivery_person_Age'] = df1['Delivery_person_Age'].astype(int) #muda o tipo da coluna

    # 2 convertendo 'Delivery_person_Ratings' em flutuante (decimal)
    df1['Delivery_person_Ratings'] = df1['Delivery_person_Ratings'].astype(float) 

    # 3 convertendo 'Order_Date' em data
    df1['Order_Date'] = pd.to_datetime(df1['Order_Date'],format= '%d-%m-%Y') 

    #4 multiple_deliveries 'Type_of_vehicle' em numero
    retorno = df1['multiple_deliveries'] != 'NaN '
    df1['multiple_deliveries'] = retorno.astype(int)

    #6 cria semana 
    df1['Week_of_year'] = df1['Order_Date'].dt.strftime('%U') # strftime formata a data para semana do ano. (%u)   começa no domingo. 

    linha_selecionar = df1['City'] != 'NaN ' #não seleciona linha incompativel 'Nan'
    df1 = df1.loc[linha_selecionar, :].copy()

    linha_selecionar = df1['Festival'] != 'NaN ' #não seleciona linha incompativel 'Nan'
    df1 = df1.loc[linha_selecionar, :].copy()

    #5 tirando os espaços dentro de textos (primeiro, certificar que a coluna tem espaços) Outra forma
    df1.loc[:,'ID'] = df1.loc[:, 'ID'].str.strip()
    df1.loc[:,'Delivery_person_ID'] = df1.loc[:, 'Delivery_person_ID'].str.strip()
    df1.loc[:,'Road_traffic_density'] = df1.loc[:, 'Road_traffic_density'].str.strip()
    df1.loc[:,'Type_of_order'] = df1.loc[:, 'Type_of_order'].str.strip()
    df1.loc[:,'Type_of_vehicle'] = df1.loc[:, 'Type_of_vehicle'].str.strip()
    df1.loc[:,'Festival'] = df1.loc[:, 'Festival'].str.strip()
    df1.loc[:,'City'] = df1.loc[:, 'City'].str.strip()
    df1.loc[:,'ID'] = df1.loc[:, 'ID'].str.strip()


    #substitui
    df1['Time_taken(min)'] = df1['Time_taken(min)'].apply( lambda x: x.split( '(min) ')[1] )
    df1['Time_taken(min)'] = df1['Time_taken(min)'].astype(int)

    return df1
#==============================================================================================================

#importe dataset
df1 = pd.read_csv(r'dataset/train.csv' )

#limpando dados
df1=clean_code(df1)

#retirar NaN

#=======================================================================================
#                               BARRA LATERAL
#=======================================================================================
st.header('MarketPlace - Visão Entregadores')

image_path = 'logo.png'
image = Image.open(image_path)
st.image(image, width=120)


st.sidebar.markdown('# Cury Companany')
st.sidebar.markdown('## Fasted Delivery in Town')
st.sidebar.markdown("""____""")
st.sidebar.markdown('## Selecione uma data limite')

date_slider = st.sidebar.slider(
    'Até qual valor?',
    value=dt.datetime( 2022,4,13),
    min_value=dt.datetime(2022, 2,11),
    max_value=dt.datetime(2022, 4, 6),
    format='DD/MM/YYYY')



#st.header(date_slider)
st.sidebar.markdown( """___""")


traffic_options = st.sidebar.multiselect(
    'Quais as condições do transito',
    ['Low','Medium', 'High', 'Jam'],
    default=['Low','Medium', 'High', 'Jam'])


st.sidebar.markdown( """___""")
st.sidebar.markdown('## Powered by Comunidade DS')
#----------------------------------------------------
#aplictando filtro de data (data slider)
linhas_selecionadas = df1['Order_Date'] < date_slider
df1 = df1.loc[linhas_selecionadas, :]
#teste
#st.dataframe(df1)


#aplictando filtro de data (data slider)------------------------------------
linhas_selecionadas = df1['Road_traffic_density'].isin(traffic_options)
df1 = df1.loc[linhas_selecionadas, :]
#teste
#st.dataframe(df1)




#=======================================================================================
#                             LAYOUT nos stremlit
#=======================================================================================
tab1, tab2, tab3 = st.tabs(['Visão Gerencial','_','_'])

with tab1:
    with st.container():
        st.title('Overall metrics')
    
        col1, col2, col3, col4= st.columns (4, gap='large')
       
        with col1:
            st.subheader('Maior idade')   
            maior = df1.loc[:, 'Delivery_person_Age'].max()
            col1.metric('Maior idade', maior)
            
            
        with col2:
            st.subheader('Menor idade')
            menor = df1.loc[:, 'Delivery_person_Age'].min()
            col2.metric('Menor idade', menor)
            
        with col3:
            st.subheader('Melhor condição')
            melhor = df1.loc[:, 'Vehicle_condition'].max()
            col3.metric('Melhor Condição', melhor)
            
            
        with col4:
            st.subheader('Pior condição')
            pior = df1.loc[:, 'Vehicle_condition'].min()
            col4.metric('Melhor Condição', pior)
            
    with st.container():
        
        st.markdown("""___""")
        
        st.title('avaliações')
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('##### avaliação media por entregador')
            avalidacao = df1.loc[:,['Delivery_person_Ratings','Delivery_person_ID']].groupby(['Delivery_person_ID']).mean().reset_index()
            st.dataframe(avalidacao)
        
        with col2:
            st.markdown('##### avaliação média por transito e desvio padrao')
            av_media_dev_padrao = (df1.loc[:, ['Delivery_person_Ratings', 'Road_traffic_density'] ]
            .groupby(['Road_traffic_density']).agg({'Delivery_person_Ratings':['mean','std']}))
            av_media_dev_padrao.columns = ['traffic_density_mean','traffic_density_std'] 
            av_media_dev_padrao=av_media_dev_padrao.reset_index()

            st.dataframe(av_media_dev_padrao)

    
            st.markdown ('##### avaliação média por condição climática')
        
            media_padrao = (df1.loc[:,['Delivery_person_Ratings','Weatherconditions']]
            .groupby(['Weatherconditions']).agg({'Delivery_person_Ratings':['mean','std']}))
            media_padrao.columns = ['weather_mean','weather_std']
            media_padrao = media_padrao.reset_index()
            st.dataframe(media_padrao)
    
    with st.container():
        st.markdown("""___""")
        
        st.title('Avaliação de Velocidade')
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("##### Top entregadores mais rápidos")
            df3 = top_entregadores(df1,top_asc=True)
            st.dataframe(df3)
            
            
            
        with col2:
            st.markdown("##### Top entregadores mais lentos")
            #está sendo utilizado o mim() antes do sort_values pois não é propriedade do groupby (não aceita)
            df3 = top_entregadores(df1,top_asc=False)
            st.dataframe(df3)
            
                            

            
            
        
        
        
        
        
        
            
            
            
            
    
