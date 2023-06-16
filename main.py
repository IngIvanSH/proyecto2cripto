import streamlit as st
from streamlit_option_menu import option_menu
import crear
import validar
import inicio
PAGE_ICON: str = "🎖️"

st.sidebar.title('Por favor, selecciona una opción:')

#sidebar menu
with st.sidebar:
    selected = option_menu("Menu Principal", ["Inicio","Crear Certificado", 'Validar Certificado'], 
        icons=['house', 'award', 'patch-check'], menu_icon="cast", default_index=1)

def main(): 
	st.set_page_config(
	        page_title="CERTIFICADOS GDI",
	        layout="wide"
	    )

if selected == 'Inicio':
    inicio.set_inicio()
elif selected == 'Crear Certificado':
    crear.set_crearCertificado()
elif selected == 'Validar Certificado':
    validar.set_validarCertificado()

