"""
Limpieza de datos usando Pandas
-----------------------------------------------------------------------------------------

Realice la limpieza del dataframe. Los tests evaluan si la limpieza fue realizada 
correctamente. Tenga en cuenta datos faltantes y duplicados.

"""



import pandas as pd
from datetime import datetime

def clean_data():
    
    df = pd.read_csv("solicitudes_credito.csv", sep=";")
    
    # Eliminar filas con datos vacíos
    columnas_a_verificar = ['tipo_de_emprendimiento','barrio','comuna_ciudadano' ]
    df_clean = df.dropna(subset=columnas_a_verificar)

    def standardize_date(date_str):
        try:
            # Analizar la fecha en diferentes formatos
            date = datetime.strptime(date_str, '%d/%m/%Y')
        except ValueError:
            try:
                date = datetime.strptime(date_str, '%Y-%m-%d')
            except ValueError:
                try:
                    date = datetime.strptime(date_str, '%Y/%m/%d')
                except ValueError:
                    # Si no coincide con ninguno de los formatos, asigna None
                    return None
        # Convierte la fecha analizada al formato deseado (por ejemplo, 'DD/MM/AAAA')
        return date.strftime('%d/%m/%Y')

    def standardize_credit_amount(amount_str):
        try:
            # Eliminar caracteres especiales y convertir a un número
            cleaned_amount = float(amount_str.replace("$", "").replace(",", ""))
            return cleaned_amount
        except (ValueError, AttributeError):
            return None  # Manejar valores no válidos

    # Realizar la transformación de la columna "monto_del_credito" después de eliminar las filas con datos vacíos
    df_clean['monto_del_credito'] = df_clean['monto_del_credito'].apply(standardize_credit_amount)
 
    # Estandarizar la columna "sexo" convirtiendo todo a minúsculas
    df_clean['sexo'] = df_clean['sexo'].str.lower()

    # Estandarizar la columna "tipo_de_emprendimiento" convirtiendo todo a minúsculas
    df_clean['tipo_de_emprendimiento'] = df_clean['tipo_de_emprendimiento'].str.lower()

    # Estandarizar la columna "idea_negocio" convirtiendo todo a minúsculas
    df_clean['idea_negocio'] = df_clean['idea_negocio'].str.lower()

    # Estandarizar la columna "línea_credito" convirtiendo todo a minúsculas
    df_clean['línea_credito'] = df_clean['línea_credito'].str.lower()

    # Estandarizar la columna "idea_negocio"
    df_clean['idea_negocio'] = df_clean['idea_negocio'].str.replace(' ', '_')  # Reemplazar espacios en blanco con _
    df_clean['idea_negocio'] = df_clean['idea_negocio'].str.replace('-', '_')  # Reemplazar guiones con _


    # Estandarizar la columna "barrio" aplicando reglas de limpieza
    df_clean['barrio'] = df_clean['barrio'].str.lower()
    df_clean['barrio'] = df_clean['barrio'].str.replace('-', '_')  # Reemplazar guiones con _
    df_clean['barrio'] = df_clean['barrio'].str.replace(' ', '_')  # Reemplazar guiones con _


    # Estandarizar la columna "línea_credito" aplicando reglas de limpieza
    df_clean['línea_credito'] = df_clean['línea_credito'].str.lower()
    df_clean['línea_credito'] = df_clean['línea_credito'].str.replace('.', '_')  # Eliminar puntos
    df_clean['línea_credito'] = df_clean['línea_credito'].str.replace(' ', '_')  # Reemplazar espacios en blanco con _
    df_clean['línea_credito'] = df_clean['línea_credito'].str.replace('-', '_')  # Reemplazar guiones con _
    df_clean['línea_credito'] = df_clean['línea_credito'].str.replace('andaluc¿a', 'andalucia')
    df_clean['línea_credito'] = df_clean['línea_credito'].str.rstrip('_')

    # Convertir la columna "comuna_ciudadano" a números enteros y asignar 0 a los valores faltantes
    df_clean['comuna_ciudadano'] = df_clean['comuna_ciudadano'].fillna(0).astype(int)

    # Estandarizar la columna "fecha_de_beneficio"
    df_clean['fecha_de_beneficio'] = df_clean['fecha_de_beneficio'].apply(standardize_date)
    
   # Encontrar las filas duplicadas en el DataFrame, excluyendo 'Unnamed: 0'
    duplicados = df_clean[df_clean.duplicated(keep=False, subset=df_clean.columns.difference(['Unnamed: 0']))]
    
    # Eliminar las filas duplicadas
    df_clean = df_clean.drop_duplicates(subset=df_clean.columns.difference(['Unnamed: 0']))

    # Restablecer el índice del DataFrame
    df_clean.reset_index(drop=True, inplace=True)

    return df_clean

