import streamlit as st

def set_inicio():
    st.title("Inicio")
    st.header('BIENVENIDO A CERTIFICADOS GDI')

    st.image("https://www.unioncdmx.mx/wp-content/uploads/2021/06/unam-mejores-universidades-1024x576.jpg",width=800)

    st.markdown('Gracias a la tecnología blockchain este sistema emite y verifica certificados académicos seguros y confiables garantizando su autenticidad e integridad, eliminando el riesgo de certificados falsos. Además, proporcionamos una interfaz intuitiva y fácil de usar, lo que facilita la emisión, consulta y verificación de los certificados.')

    st.title("Crear Certificado")
    wallpaper = st.image("https://i0.wp.com/blog.mifiel.com/wp-content/uploads/2019/11/blog-que-es-un-certificado.png?fit=1170%2C550&ssl=1",width=800)
    st.markdown('En esta sección se generará un nft en representación del certificado con la información almacenada en la base de datos de la institución académica, además se guarda el id y hash del nft. El nft generado se guarda en la blockchain, lo que asegura su integridad y proporciona una forma segura de almacenar y compartir el certificado. El cliente tendrá el id de su certificado para poder verificarlo.')
    
    st.title("Validar Certificado")
    st.image("https://flashdata.org/wp-content/uploads/2020/10/certificados_digitales-01.png",width=500)
    st.markdown('En esta sección se verifica la autenticidad del certificado con el id del certificado. Para esto se debe de ingresar ambos datos, se busca el certificado con su id, al encontrarlo se compara que el hash almacenado y el que se haya ingresado, si son iguales quiere decir que es autentico y no ha sido modificado.')