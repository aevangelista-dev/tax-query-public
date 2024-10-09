import streamlit as st
import streamlit.components.v1 as components
import pickle
import base64
import os
from datetime import datetime
from st_pages import hide_pages
import func
import msal
import pandas as pd
import pyodbc
#import pyad

desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')


st.set_page_config(page_title="Home", layout="wide",initial_sidebar_state="auto", page_icon='img/jpeg/ruah_logo_blue.png')

#st.cache(allow_output_mutation=True)
#@st.cache_data

func.apply_custom_style()   

func.hide_anchor_link()

#func.build_menu_item_bar(0)

func.set_page_title(st, "","Login")

placeholder = st.sidebar.empty()

with st.sidebar:
     html_code_bar = "<div class='menu-logo'>"
     html_code = func.get_img_with_href("img/jpeg/ruah_logo_dourado.png",'home','RUAH', 80)
     html_code_bar = html_code_bar + html_code
     
     html_code_bar = html_code_bar + "</div>"
     st.sidebar.markdown(html_code_bar,unsafe_allow_html=True)          
     st.sidebar.markdown(f"<div class='menu-title'><br><p style='font-family: Tan Pearl; color: #ffd080; font-size: 18px;'><br>RUAH TAX TECHNOLOGY</br></p></div>",unsafe_allow_html=True)          


def Init_Variables():
    #if "usr_nome" not in st.session_state:
    if  "edt_servidor" not in st.session_state:
        aconfig_values = func.read_config()    

        st.session_state.edt_servidor         = aconfig_values['db_server']
        st.session_state.edt_basedados        = aconfig_values['db_database']
        st.session_state.edt_username         = aconfig_values['db_username']
        st.session_state.edt_pwd              = aconfig_values['db_password']
        st.session_state.winauth              = bool(aconfig_values['db_winauth'])


def test_sql_conn(server, database, username, password):
    result = False
    Sql_Driver = func.get_sql_driver()
    if st.session_state.winauth:
        strConn = Sql_Driver + ";SERVER=" + server + ";DATABASE=" + database + ";Trusted_Connection=yes; MultipleActiveResultSets=True"
    else:
        strConn = Sql_Driver + ";SERVER=" + server + ";DATABASE=" + database + ";UID=" + username + ";PWD=" + password +";MultipleActiveResultSets=True"

    try:
        conn = pyodbc.connect(strConn)
        cursor = conn.cursor()
        cursor.execute('select * from sys.objects')

        func.Msg(1,"Conexão realizada com sucesso!")

        result = True  
    except Exception as e:
        func.Msg(0,"Erro ao tentar conectar: " + str(e))
        result = False
    
    return result

def show_login():
    cols = st.columns(3)        
    with cols[0]:
        st.text_input('Servidor: ', value=st.session_state.edt_servidor, key="edt_servidor")
        st.text_input('Base de Dados:', value=st.session_state.edt_basedados, key="edt_basedados")
        st.checkbox('Autenticação com Windows:', value=st.session_state.winauth, key="winauth" )
        st.text_input('Usuário:', value=st.session_state.edt_username, key="edt_username")
        st.text_input('Senha:', value=st.session_state.edt_pwd, type="password", key="edt_pwd" )

        btnConectar = st.button("Conectar")

        if btnConectar:
            if st.session_state.edt_servidor == "":
               func.Msg(0,"Servidor não informado!")
               st.stop()

            if st.session_state.edt_basedados == "":
               func.Msg(0,"Base de dados não informada!")
               st.stop()
                
            if not st.session_state.winauth and st.session_state.edt_username =="" :
               func.Msg(0,"Usuário não informado!")
               st.stop()

            if not st.session_state.winauth and st.session_state.edt_pwd =="" :
               func.Msg(0,"Senha não informado!")
               st.stop()

            if  test_sql_conn(st.session_state.edt_servidor, st.session_state.edt_basedados, st.session_state.edt_username,  st.session_state.edt_pwd):
                aRetorno = func.write_config(st.session_state.edt_basedados, st.session_state.edt_servidor, st.session_state.winauth, st.session_state.edt_username, st.session_state.edt_pwd) 
                #st.write(aRetorno)
                if aRetorno[0]  == 1: 
                   st.switch_page("pages/tax_query.py")   

#Inicializa as variáveis
Init_Variables()

#Mostra a tela de logon
show_login()



