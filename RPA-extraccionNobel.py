import pandas as pd
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait

#Configuraciones del navegador por Default
options = Options() 
options.headless = True

def selenium(browser, final_path):
    '''
    [Seguridad]

    1. Categoria
        
    2. Impacto operativo
        
    3. Scope
        Bases de datos. 
    4. Complejidad del desarrollo
        Complejidad Baja

    [Descripcion]
    
    Obtener el listado de los ganadores del Premio Nobel a lo largo de la historia desde Wikipedia

    [Creación]

        1. Autor:  Daniel Garzon
        2. Dia de Creación: 3/8/2023
        3. Incident: Desarrollador Junior

    [Modificación]

        1. Autor:  - 
        2. Dia de modificación: 
        3. Incident: 
        4. Descripcion:  

    [Proceso]

        1. Intancia el navegador Mozilla y lo inicializa
        2. Busca mediante Xpath la Tabla dentro del codigo HTML
        3. Busca los elementos que se encuentran en esa tabla y los transforma 
        4. Genera un archivo CSV con los datos
        5. Escribe un mensaje por consola para verificar si el proceso se completo exitosamente
            
    [Funciones]

        save_to_csv: guarda los datos extraidos en formato CSV  

    '''
    #------------------------------------
    # FUNCIONES
    #------------------------------------
    def save_to_csv(headers, data, file_name):
        df = pd.DataFrame(data, columns=headers)
        df.to_csv(f"{final_path}/{file_name}.csv", index=False, encoding='utf-8')
        print(f"Los datos han sido guardados en {final_path}/{file_name}.csv")

    #------------------------------------
    # VARIABLES DE CONFIGURACION
    #----------------------------------------------------------------------------------------------------------------------------
    url = "https://es.wikipedia.org/wiki/Anexo:Ganadores_del_Premio_Nobel"
    #----------------------------------------------------------------------------------------------------------------------------
    data = []
    wait= WebDriverWait(browser, 60)
    # Abrir la página
    try:
        browser.get(url)    

        # Encuentra la tabla de los ganadores del Premio Nobel en el HTML por ID unico
        table_element = browser.find_element(By.ID, "mw-content-text")
        
        # Obtener los datos del thead y tfooter con la misma etiqueta
        header_footer = [data.text.replace("\n", " ") for data in table_element.find_elements(By.XPATH , ".//th")]

        # Los primeros 7 correponden al Header, los 7 restantes al Foteer
        headers = header_footer[:7]
        footer = header_footer[7:]

        # Obtener los datos de las filas
        rows = table_element.find_elements(By.XPATH ,".//tr")[1:-1]
        
        # Estructurar datos en filas 
        for row in rows:
            row_data = [cell.text.replace("\n", " ") for cell in row.find_elements(By.XPATH ,".//td")]
            data.append(row_data)
        data.append(footer)

        # Cierra el navegador
        browser.quit()

        # Exportar data a CSV format
        try:
            save_to_csv(headers,data,"ganadores_Nobel")
        except: 
            print("No se pudo guardar la informacion")
    except:
        print("error inesperado o el ID de la tabla cambio")




if __name__ == "__main__":
    # Obtiene el path absoluto del archivo actual (el script de Python que se está ejecutando)
    archivo_actual = os.path.abspath(__file__)

    # Obtiene el directorio padre del archivo actual (la carpeta que contiene el script)
    carpeta_actual = os.path.dirname(archivo_actual)

    # El path relativo de la carpeta en relación con el directorio de trabajo actual
    final_path = os.path.relpath(carpeta_actual)

    # Configura el navegador a utilizar e inicia el proceso
    browser = webdriver.Firefox(options=options)
    selenium(browser,final_path)

