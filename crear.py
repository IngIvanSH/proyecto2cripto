import streamlit as st
import hashlib
from algosdk import transaction
from algosdk.v2client import algod
from algosdk import account, mnemonic, encoding
from algosdk.transaction import *
from PIL import Image, ImageDraw, ImageFont
import sqlite3
import random

def set_crearCertificado():
    st.title("Creando Certificado")
    st.markdown('Ingresa tu número de cuenta: ')
    busquedaUsuario = st.text_input('Número de cuenta')
    print("tipo: ",type(busquedaUsuario))
    
    boton1 = st.button('Crear mi certificado')

    if boton1:
        miConexion=sqlite3.connect("BaseEstudiantes")
        cursor=miConexion.cursor()
        cursor.execute("SELECT * FROM ESTUDIANTES WHERE num_cuenta = ?", ((int(busquedaUsuario)),))
        str_match=cursor.fetchall()
        if len(str_match) != 0:
            st.info('Creando certificado...')
            #recuperamos los datos del usuario
            datosUsuario = str_match[0]
            
            #creamos el diccionario certificado
            certificado = {"nombre": datosUsuario[1], 
                    "promedio": datosUsuario[2], 
                    "carrera": datosUsuario[3], 
                    "institución": datosUsuario[4],
                    "numero de cuenta": datosUsuario[0], 
                    "ID-Asset": None}
            
            #Pruebas
            mnemonic1 = "dream object fall athlete black broken equip just love express image sister useful guitar angle strong near mass beach slight hole kiss flee abstract target"
            address1 = "X5GKBQG5KHWXGRWTYITXI56EDX4SLZZNS3MMFTRFJVJWQMDDCF6JJ367TU"
            
            cuentaUsuario = datosUsuario[7]

            #SOLO FINAAAAAAAAAL
            """
            mnemonic1 = 'load silk plastic orbit neither sugar grid roast cream brisk note ship salad whale trouble concert under shove empower present expose verb afford above sail'
            address1 = '7KHQ2JFNE3KPPCBBTOOTRHYBWC2JXLQKBMD3TKJNMYOV6MGVAYUGGYRDVU'
            """

            # Obtenemos las llaves privadas usando mnemónicos
            sk = "{}".format(mnemonic.to_private_key(mnemonic1))
            sk1 = "{}".format(mnemonic.to_private_key(datosUsuario[6]))

            # Configurar la conexión a la red de Algorand
            algod_client = algod.AlgodClient(
                algod_token="",
                algod_address="https://testnet-algorand.api.purestake.io/ps2",
                headers={"X-API-Key": "ENKbXOMzG31nVpzbBz3Oiap27mQK9oNp7Of480pb"}
            )

            #parámetros del NFT
            params = algod_client.suggested_params()
            params.fee = 1000
            params.flat_fee = True

            #creamos el hash
            numRandom = random.randint(0, 1000000)
            data_as_text = (str(datosUsuario[0]+numRandom))
            data_hash = hashlib.sha256(data_as_text.encode())

            txn = AssetConfigTxn(
                sender=address1,
                sp=params,
                total=1,
                default_frozen=False,
                unit_name="cert",
                asset_name="CertificadoEscolar",
                manager=address1,
                reserve=cuentaUsuario,
                freeze=address1,
                clawback=address1,
                url="https://path/to/my/asset/details",
                metadata_hash=data_hash.digest(),
                decimals=0)
            stxn = txn.sign("{}".format(sk))

            try:
                txid = algod_client.send_transaction(stxn)
                print("Signed transaction with txID: {}".format(txid))
                confirmed_txn = wait_for_confirmation(algod_client, txid, 4)
                print("TXID: ", txid)
                print("Result confirmed in round: {}".format(confirmed_txn['confirmed-round']))
                
                results = transaction.wait_for_confirmation(algod_client, txid, 4)
                print(f"Result confirmed in round: {results['confirmed-round']}")

                created_asset = results["asset-index"]
                print(f"Asset ID created: {created_asset}")

                #modificamos el hash del diccionario
                certificado["ID-Asset"] = created_asset

                #añadimos el id_asset del estudiante
                cursor.execute("UPDATE ESTUDIANTES SET ID_ASSET = ? WHERE num_cuenta = ?", (str(created_asset), busquedaUsuario))
                miConexion.commit()

                #imprimimos todos los datos
                print(certificado)

                account_info = algod_client.account_info(cuentaUsuario)
                holding = None
                idx = 0
                for my_account_info in account_info['assets']:
                    scrutinized_asset = account_info['assets'][idx]
                    idx = idx + 1
                    if (scrutinized_asset['asset-id'] == created_asset):
                        holding = True
                        break
                if not holding:
                # Usamos la clase AssetTransferTxn para transferir y realizar opt-in
                    txn = AssetTransferTxn(
                        sender=cuentaUsuario,
                        sp=params,
                        receiver=cuentaUsuario,
                        amt=0,
                        index=created_asset)
                    stxn = txn.sign(sk1)
                    # Se envia la transacción a la red
                    try:
                        txid = algod_client.send_transaction(stxn)
                        print("Signed transaction with txID: {}".format(txid))
                        confirmed_txn = wait_for_confirmation(algod_client, txid, 4)
                        print("TXID: ", txid)
                        print("Result confirmed in round: {}".format(confirmed_txn['confirmed-round']))

                        txn = AssetTransferTxn(
                            sender="X5GKBQG5KHWXGRWTYITXI56EDX4SLZZNS3MMFTRFJVJWQMDDCF6JJ367TU",
                            sp=params,
                            receiver=cuentaUsuario,
                            amt=1,
                            index=created_asset)
                        stxn = txn.sign(sk)
                        # Se envia la transacción a la red
                        try:
                            txid = algod_client.send_transaction(stxn)
                            print("Signed transaction with txID: {}".format(txid))
                            # Wait for the transaction to be confirmed
                            confirmed_txn = wait_for_confirmation(algod_client, txid, 4)
                            print("TXID: ", txid)
                            print("Result confirmed in round: {}".format(confirmed_txn['confirmed-round']))
                            
                        except Exception as err:
                            print(err)
                    except Exception as err:
                        print(err)
            except Exception as err:
                print(err)

            st.success('Número de cuenta válido. Certificado creado')
            
            # Llamar a la función para generar el certificado
            generar_certificado(datosUsuario,str(created_asset))

            imagen_cert = "certificado_generado.png"
            st.image(imagen_cert, caption="Certificado")

            # Cargar la imagen
            imagen_bytes = open(imagen_cert, "rb").read()
            
            cadena = 'La clave asociada con el Certificado es: '+str(created_asset)
            st.warning(cadena)
            st.write('Esta clave es la que servirá para verificar tu certificado dentro de las transacciones de blockchain')

            cadena = 'El link para consultar tu nft dentro de Algorand es el siguiente: https://testnet.algoexplorer.io/asset/'+str(created_asset)
            st.info(cadena)

            # Mostrar el botón de descarga
            st.download_button("Descargar Certificado", data=imagen_bytes, file_name="certificado.png", mime="image/png")
            
        else:
            st.error('El número de cuenta ingresado no es valido o no existe en los registros')

        #cerramos la conexión a la base de datos
        miConexion.close()

# Función para generar un certificado con los datos ingresados por el usuario
def generar_certificado(datosUsuario,id):
    nombre = datosUsuario[1]
    carrera = datosUsuario[3]
    numcuenta = str(datosUsuario[0])
    promedio=datosUsuario[2]

    # Cargar la imagen del certificado base
    certificado = Image.open("certificado_base.png")

    # Crear un objeto ImageDraw para dibujar en la imagen
    draw = ImageDraw.Draw(certificado)

    # Cargar una fuente de texto
    fuente_nombre = ImageFont.truetype("arial.pil", size=70)
    fuente = ImageFont.truetype("arial.pil", size=40)

    # Escribir los datos en el certificado
    draw.text((620, 600),  nombre, font=fuente_nombre, fill=(0, 0, 0))
    draw.text((680, 890),  carrera, font=fuente, fill=(0, 0, 0))
    draw.text((1050, 770),  numcuenta, font=fuente, fill=(0, 0, 0))
    draw.text((950, 835),  promedio, font=fuente, fill=(0, 0, 0))
    draw.text((100, 1330),  id, font=fuente, fill=(0, 0, 0))

    # Guardar el certificado generado
    certificado.save("certificado_generado.png")

