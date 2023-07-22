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
import numpy as np
import plotly.express as px
import streamlit as st
from PIL import Image
from streamlit_folium import folium_static
import plotly.graph_objects as go

st.set_page_config( page_title='Visão Restaurante', page_icon='', layout='wide')

#===================================================================
#                        Bloco de Funções
#=====================================================================


def avg_std_city_traffic(df1):

    df_aux = (df1.loc[:,['Time_taken(min)','City','Road_traffic_density']]
                  .groupby(['City','Road_traffic_density'])
                  .agg({'Time_taken(min)':['mean','std']}))
    df_aux.columns=['avg_time','std_time']
    df_aux=df_aux.reset_index()
    fig=px.sunburst(df_aux, path=['City','Road_traffic_density'], values= 'avg_time', 
                    color='std_time', color_continuous_scale='RdBu',
                    color_continuous_midpoint=np.average(df_aux['std_time']))

    return(fig)


def avg_std_time_graph(df1):
    df_aux = df1.loc[:,['Time_taken(min)','City']].groupby('City').agg({'Time_taken(min)':['mean','std']})
    df_aux.columns = ['avg_time','std_time']
    df_aux=df_aux.reset_index()
    fig = go.Figure() 
    fig.add_trace(go.Bar(name = 'Control',
    x=df_aux['City'],
    y=df_aux['avg_time'],
    error_y=dict(type='data',array=df_aux['avg_time'])))
    fig.update_layout(barmode='group')

    return fig



def time_in_festival(df1, festival, op):
    """
        esta função calcula  o tempo médio eo desvio padrao do tempo de entrega.
        parametros:
            imput:
                -df: dataframe com os dados necessários para o calculo
                -op: tipo de operação que precisa ser calculado
                    'avg_time': calcula o tempo médio
                    'std_time': calcula o desvio padrao do tempo.
           Output:
               -df: dataframe 2 colunas e 1 linha
    """

    df_aux = (df1.loc[:, ['Time_taken(min)', 'Festival']]
               .groupby(['Festival'])
               .agg({'Time_taken(min)' : ['mean','std']}))

    df_aux.columns = ['avg_time','std_time']
    df_aux=df_aux.reset_index()

    df_aux = np.round(df_aux.loc[df_aux['Festival'] == festival, op],2) 


    return df_aux



def distancia(df1,fig):
    if fig==False:
        cols=['Restaurant_latitude','Restaurant_longitude','Delivery_location_latitude','Delivery_location_longitude']
        df1['distance'] = df1.loc[:, cols].apply(lambda x: 
                                    haversine ((x['Restaurant_latitude'], x['Restaurant_longitude']),
                                    (x['Delivery_location_latitude'], x['Delivery_location_longitude']) ),axis=1 )

        avg_distance = np.round(df1['distance'].mean(),2)
        return avg_distance

    else:
        cols=['Restaurant_latitude','Restaurant_longitude','Delivery_location_latitude','Delivery_location_longitude']
        df1['distance'] = df1.loc[:, cols].apply(lambda x:
                            haversine((x['Restaurant_latitude'], x['Restaurant_longitude']),
                            (x['Delivery_location_latitude'], x['Delivery_location_longitude']) ),axis=1 )

        avg_distance = df1.loc[:,['City','distance']].groupby('City').mean().reset_index()

        fig = go.Figure(data=[go.Pie( labels=avg_distance['City'], values=avg_distance['distance'], pull=[0, 0.1, 0])])
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
df1 = pd.read_csv(r'dataset\train.csv' )

#limpando dados
df1=clean_code(df1)

#retirar NaN



#retirar NaN

#=======================================================================================
#                               BARRA LATERAL
#=======================================================================================
st.header('MarketPlace - Visão Restaurante')

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
        col1,col2,col3,col4,col5,col6 = st.columns(6)
        with col1:
            #st.markdown('#### Entregadores unicos')
            df2 = df1['Delivery_person_ID'].unique()
            col1.metric('Total Entregadores',len(df2))
            
        with col2:
            #st.markdown('#### distancia media')
            avg_distance = distancia(df1,fig=False)
            col2.metric('distancia media',avg_distance)
            
                
        with col3:
           
            df_aux = time_in_festival(df1,'Yes', 'avg_time')                                 
            col3.metric('Tempo Medio c/F',df_aux)                                  
                                             
            
        with col4:
            
            df_aux = time_in_festival(df1,'Yes','std_time')                                 
            col4.metric('Desvio Padrao c/F',df_aux)          
            
            
        with col5:
            #st.markdown('#### temp entrega médiao S/ festival')
            df_aux = time_in_festival(df1,'No','avg_time') 
            col5.metric('Tempo Medio s/F',df_aux)

        with col6:
            #st.markdown('#### desvio padrao de entrega medio s/ festival')
                                      
            df_aux = time_in_festival(df1,'No','std_time') 
            col6.metric('Std s.festival',df_aux)

            
    with st.container():
        st.markdown("""___""")
        st.markdown('#### distribuição do tempo por cidade')
        
        col1, col2 = st.columns(2)
        
        with col1:
           
            fig = avg_std_time_graph(df1)
            st.plotly_chart(fig)
            
        with col2:
             
            df2 = df1.loc[:,['Time_taken(min)','City','Type_of_order']].groupby(['City','Type_of_order']).agg({'Time_taken(min)':['mean','std']})

            df2.columns = ['avg_time','std_time']
            df2 = df2.reset_index()
            st.dataframe(df2)

        
    with st.container():
        st.markdown("""___""")
        #st.title('distribuição por tempo')  
        
        col1,col2 = st.columns(2)
        with col1:
            fig_ = distancia(df1, fig=True)
            st.plotly_chart(fig_)
            
        with col2:
            
            fig = avg_std_city_traffic(df1)
            st.plotly_chart(fig)
            
            
         
   # with st.container():
   #     st.markdown("""___""")
   #     st.title('tempo medio por cidade e tipo de trafego')