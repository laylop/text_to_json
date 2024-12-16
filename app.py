import re
import json

# Leer el texto desde el archivo input_text.txt

with open('input_text.txt', 'r', encoding='utf-8') as file:
    texto = file.read()

# Función para procesar el texto plano


def procesar_texto(texto, start_id=1):
    # Dividir el texto en bloques de clubes individuales
    bloques_clubes = re.split(r'\n\n(?=Name:)', texto.strip())

    # Lista para almacenar los resultados procesados
    result = []

    # Para cada bloque de club, extraemos la información
    for index, bloque in enumerate(bloques_clubes):
        # Extraer nombre
        match_nombre = re.search(r"Name:\s*(.*?)(?=\n)", bloque)
        nombre = match_nombre.group(1).strip() if match_nombre else ""

        # Extraer dirección específicamente de este bloque
        match_direccion = re.search(
            r"Dirección\s*[:\s]*(.*?)(?=\n\w+:|\n\n|$)", bloque, re.DOTALL)
        direccion = match_direccion.group(1).strip().replace(
            '\n', ' ') if match_direccion else ""

        # Extraer teléfono
        match_telefono = re.search(
            r"Teléfono\s*[:\s]*(.*?)(?=\n\w+:|\n\n|$)", bloque)
        telefono = match_telefono.group(1).strip() if match_telefono else ""

        # Extraer web
        match_web = re.search(r"Web\s*[:\s]*(.*?)(?=\n\w+:|\n\n|$)", bloque)
        web = match_web.group(1).strip() if match_web else ""
        if web and not web.startswith("https://"):
            web = "https://" + web if web else ""

        # Extraer email - MODIFICADO
        match_email = re.search(
            r"Email\s*[:\s]*(.*?)(?=\n(?:Número de hoyos|Name:|Web:|Teléfono:)|$)", bloque, re.DOTALL)
        email = match_email.group(1).strip() if match_email else ""

        # Extraer número de hoyos
        match_hoyos = re.search(
            r"Número de hoyos\s*[:\s]*(.*?)(?=\n\n|$)", bloque)
        numero_hoyos = match_hoyos.group(1).strip() if match_hoyos else ""

        # Crear el objeto con los datos extraídos
        club_golf = {
            "id": start_id + index,
            "img": "",  # Este campo está vacío
            "name": nombre,
            "direccion": direccion,
            "telefono": telefono,
            "web": web,
            "email": email,
            "numero_hoyos": numero_hoyos
        }

        # Agregar el club a la lista de resultados
        result.append(club_golf)

    return result


# Procesar el texto
datos_procesados = procesar_texto(texto)

# Guardar el resultado en un archivo JSON
with open('text.json', 'w', encoding='utf-8') as f:
    json.dump(datos_procesados, f, indent=2, ensure_ascii=False)

print("Los datos se han guardado en 'text.json'.")
