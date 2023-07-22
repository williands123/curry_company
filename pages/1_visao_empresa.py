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

#===================================================================
#                        Bloco de Funções
#=====================================================================

#função para que a figura ou gráfico fique espandida
st.set_page_config( page_title='Visão Empresa', page_icon='', layout='wide')



def country_maps(df1):
    df_aux = df1.loc[:,['City','Delivery_location_latitude','Delivery_location_longitude','Road_traffic_density']].groupby(
    ['City','Road_traffic_density']).median().reset_index()
    df_aux = df_aux[df_aux['City'] != 'NaN']
    df_aux = df_aux[df_aux['Road_traffic_density'] != 'NaN']
    map_ = folium.Map()

    for index, location_info in df_aux.iterrows():
        folium.Marker( [location_info['Delivery_location_latitude'],
        location_info['Delivery_location_longitude']],
        popup=location_info[['City', 'Road_traffic_density']] ).add_to( map_ )

    folium_static(map_, width =1024, height=600)

    return None


def order_share_week(df1):

    df_aux1 = df1.loc[:,['ID','Week_of_year']].groupby(['Week_of_year']).count().reset_index()
    #Qtd Entregadores unicos por semana
    df_aux2 = df1.loc[:,['Delivery_person_ID','Week_of_year']].groupby(['Week_of_year']).nunique().reset_index()
    #juntar as colunas
    df_aux = pd.merge(df_aux1, df_aux2, how='inner')
    #cria coluna 'order_by_delivery e faz a divisão para achar a quantidade por entregador e por semana
    df_aux['order_by_delivery'] = df_aux['ID'] / df_aux['Delivery_person_ID']
    fig=px.line( df_aux, x='Week_of_year' , y='order_by_delivery' )
    return fig


def order_by_weed(df1):
    df1['Week_of_year'] = df1['Order_Date'].dt.strftime('%U') # strftime formata a data para semana do ano. (%u) começa no domingo.
    df_aux = df1.loc[:,['ID','Week_of_year']].groupby(['Week_of_year']).count().reset_index()
    fig = px.line(df_aux, x='Week_of_year', y='ID')
    return fig


def traffic_order_city(df1):
    df2 = df1.loc[:,['ID','Road_traffic_density','City']].groupby(['Road_traffic_density','City']).count().reset_index()
    fig=px.scatter(df2, x='City', y='Road_traffic_density', size='ID', color='City' ) 
    return fig


def traffic_order_share(df1):
    df_aux = df1.loc[:, ['ID','Road_traffic_density']].groupby('Road_traffic_density').count().reset_index()
    df_aux = df_aux.loc[df_aux['Road_traffic_density'] !='NaN', :] #exlcui o Nan
    df_aux['percentual_entrega'] = df_aux['ID'] / df_aux['ID'].sum() # faz a divisão para encontrar             
    fig=px.pie(df_aux , values='percentual_entrega', names='Road_traffic_density')
    return fig


def order_metric(df1): #order metric         
    df2 = df1.loc[:, ['ID', 'Order_Date']].groupby(['Order_Date']).count().reset_index()   
    fig = px.bar(df2, x= 'Order_Date', y='ID')       
    return fig

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
df1 = pd.read_csv(r'..\dataset\train.csv' )

#limpando dados
df1=clean_code(df1)
    
#=======================================================================================
#                               BARRA LATERAL
#=======================================================================================
st.header('MarketPlace - Visão Empresa')

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

tab1, tab2, tab3 = st.tabs(['Visão Gerencial','Visão Tática','Visão Geográfica'])

with tab1:
    with st.container():
        st.markdown('# Orders By Day')
        
        fig = order_metric(df1)
        #plota o gráfico de barras
        st.plotly_chart(fig, use_container_width=True)
                
        
    with st.container():
        col1, col2 = st.columns(2)   
        
        #Gráfico de pizza
        with col1:
            st.header('Traffic Order Share')
            fig = traffic_order_share(df1)
            st.plotly_chart(fig, use_container_width=True)
            
                        
        with col2:
            fig = traffic_order_city(df1)
            st.plotly_chart(fig, use_container_widht=True)
            
            
with tab2:
    with st.container():
        st.markdown('# Order By Week')
        fig = order_by_weed(df1)
        st.plotly_chart(fig, use_container_widht=True)
    
    with st.container():
        
        st.markdown('# Order By share Week')
        fig = order_share_week(df1)
        st.plotly_chart(fig, use_container_widht=True)
        
        
with tab3:
    st.markdown('Country Maps')
    country_maps(df1)
    
   
