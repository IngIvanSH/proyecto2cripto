import streamlit as st
import hashlib
from algosdk import transaction
from algosdk.v2client import algod
from algosdk import account, mnemonic, encoding
from algosdk.transaction import *
import sqlite3

def set_validarCertificado():
    st.title("Validar Certificado")
    st.image("https://flashdata.org/wp-content/uploads/2020/10/certificados_digitales-01.png",width=500)

    st.markdown('Ingresa el ID asociado con el certificado que deseas validar: ')

    busquedaUsuario = st.text_input('Clave de certificación')

    boton1 = st.button('Validar certificado')

    if boton1:
        miConexion= sqlite3.connect("BaseEstudiantes")
        cursor=miConexion.cursor()
        cursor.execute("SELECT * FROM ESTUDIANTES WHERE ID_ASSET = ?", (str(busquedaUsuario),))
        str_match=cursor.fetchall()

        if (len(str_match)!= 0):
            print("Si encontró")
            #recuperamos los datos del usuario
            datosUsuario = str_match[0]
            
            # Crear una instancia del cliente Algod
            algod_client = algod.AlgodClient(
                algod_token="",
                algod_address="https://testnet-algorand.api.purestake.io/ps2",
                headers={"X-API-Key": "ENKbXOMzG31nVpzbBz3Oiap27mQK9oNp7Of480pb"}
            )

            # ID del Asset (NFT) que deseas validar
            asset_id = busquedaUsuario
            try:
                # Obtener información del Asset (NFT)
                asset_info = algod_client.asset_info(asset_id)

                # Verificar si el Asset es un NFT
                if asset_info.get("params", {}).get("decimals") == 0:
                    print("El certificado es válido")
                    st.success('Certificado encontrado y validado')
                st.write('El certificado ingresado ha sido encontrado y validado')
                st.write('El número de cuenta asociado al certificado ingresado es: ', datosUsuario[0])
                certificado = 'certificado'
                st.write('El nombre asociado al certificado es: ', datosUsuario[1])
                claveCert = 'Clave del certificado'
                st.write('El promedio asociado al certificado ingresado es: ', datosUsuario[2])
                st.write('Con la clave asociada al certificado podrás verificar su autenticidad e integridad dentro de Blockchain')
                cadena = 'El link para consultar tu nft dentro de Algorand es el siguiente: https://testnet.algoexplorer.io/asset/'+str(asset_id)
                st.info(cadena)            
            except:
                print("El certificado no es válido porque no se encontró en Algorand")
        else:
            st.error('El certificado no es válido porque no se encuentra en la base de datos')
            print("El certificado no es válido porque no se encuentra en la base de datos")

        miConexion.close()
            

            
            
    
    

