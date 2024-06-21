import mysql.connector
from mysql.connector import Error
import json
from flask import jsonify, request

def get_database_connection():
    database = mysql.connector.connect(
        host='bdkdtfq5puosmgeju7hb-mysql.services.clever-cloud.com',
        user='uhgk69rpcuigf3bb',
        password='mPjDuU6vntiu1n1JooCQ',
        database='bdkdtfq5puosmgeju7hb'
    )
    return database
#########################################

####################

def get_num_ninos():
    database = get_database_connection()
    cursor = database.cursor()
    cursor.execute("SELECT COUNT(*) FROM niños")
    num_ninos = cursor.fetchone()[0]
    cursor.close()
    database.close()
    return num_ninos

def reporte_hg():
    database = get_database_connection()
    cursor = database.cursor()
    cursor.execute("SELECT COUNT(*) FROM reportehemoglobina")
    num_reporte = cursor.fetchone()[0]
    cursor.close()
    database.close()
    return num_reporte
####Establecimientos

def ninos_por_establecimiento():
    database = get_database_connection()
    cursor = database.cursor()
    cursor.execute("""
                   SELECT e.descripcionEsta, COUNT(*) FROM niños n INNER JOIN establecimiento e 
                   ON n.idEstablecimiento = e.idEstablecimiento WHERE e.descripcionEsta 
                   IN ('P.S HUAHUARI','P.S RIO NEGRO','P.S VILLA CAPIRI','P.S RIO CHARI ALTO',
                       'P.S PITOCUNA','P.S PUENTE IPOKI','P.S ALTO PITOCUNA','P.S CUSHIVIANI',
                       'P.S UNION CUBIRIAKI','P.S SHABASHIPANGO','P.S SAN JUA CHENI',
                       'P.S UNION CAPIRI','P.S MIGUEL GRAU','P.S ALTO VILLA VICTORIA') 
                       GROUP BY e.descripcionEsta;
""")
    num_ninos_por_establecimiento = cursor.fetchall()
    cursor.close()
    database.close()
    
    # Inicializar listas vacías para los nombres de establecimientos y números de niños
    establecimientos = []
    num_ninosEsta = []

    # Iterar sobre los resultados de la consulta y agregar los datos a las listas
    for row in num_ninos_por_establecimiento:
        establecimientos.append(row[0])
        num_ninosEsta.append(row[1])

    # Crear un diccionario con las listas y convertirlo a JSON
    data = {
        "establecimientos": establecimientos,
        "num_ninosEsta": num_ninosEsta
    }
    data_json = json.dumps(data)

    return data_json

def grafico_hg():
    database = get_database_connection()
    cursor = database.cursor()
    cursor.execute("""
                  SELECT  HG_last, fecha_last
FROM (
    SELECT 
        r.idMenor,
        MAX(CASE 
            WHEN HG4 IS NOT NULL AND HG4 <= 11.0 THEN HG4 
            WHEN HG3 IS NOT NULL AND HG3 <= 11.0 THEN HG3 
            WHEN HG2 IS NOT NULL AND HG2 <= 11.0 THEN HG2 
            WHEN HG1 <= 11.0 THEN HG1 
            ELSE NULL 
        END) AS HG_last, 
        MAX(CASE 
            WHEN HG4 IS NOT NULL AND HG4 <= 11.0 THEN fecha4 
            WHEN HG3 IS NOT NULL AND HG3 <= 11.0 THEN fecha3 
            WHEN HG2 IS NOT NULL AND HG2 <= 11.0 THEN fecha2 
            WHEN HG1 <= 11.0 THEN fecha1 
            ELSE NULL 
        END) AS fecha_last
    FROM 
        reportehemoglobina r
    WHERE 
        (HG4 IS NOT NULL AND HG4 <= 11.0 AND fecha4 IS NOT NULL) OR
        (HG3 IS NOT NULL AND HG3 <= 11.0 AND fecha3 IS NOT NULL) OR
        (HG2 IS NOT NULL AND HG2 <= 11.0 AND fecha2 IS NOT NULL) OR
        (HG1 <= 11.0 AND fecha1 IS NOT NULL)
    GROUP BY 
        r.idMenor
) AS subconsulta
WHERE 
    HG_last IS NOT NULL AND fecha_last IS NOT NULL;

                   """)
    reportes_de_hg = cursor.fetchall()
    cursor.close()
    database.close()
    
    # Inicializar listas vacías para los nombres de establecimientos y números de niños
    fechas = []
    hg_fechas = []

    # Iterar sobre los resultados de la consulta y agregar los datos a las listas
    for row in reportes_de_hg:
        fecha_completa = row[1]  # Obteniendo la fecha y hora de la segunda posición de la tupla
        if fecha_completa is not None:
            fecha_solo = fecha_completa.split()[0]  # Dividir la cadena en partes y seleccionar solo la parte de la fecha
            fechas.append(fecha_solo)
        else:
            fechas.append(None)  # Si el segundo elemento es None, agregamos None a la lista de fechas
        hg_fechas.append(row[0])

    for row in reportes_de_hg:
        print(row)

    # Crear un diccionario con las listas y convertirlo a JSON
    data = {
        "fechas": fechas,
        "num_anemia": hg_fechas
    }
    data_json = json.dumps(data)

    return data_json

def consultar_padron():
    database = get_database_connection()
    cursor = database.cursor()
    cursor.execute("""
    SELECT niños.*, 
        sexo.descripcionSexo AS sexo_descripcion, 
        establecimiento.descripcionEsta AS establecimiento_descripcion,
        CASE 
            WHEN TIMESTAMPDIFF(DAY, STR_TO_DATE(niños.fechaNacimiento, '%Y-%m-%d'), DATE(NOW())) < 30 THEN
                CONCAT(TIMESTAMPDIFF(DAY, STR_TO_DATE(niños.fechaNacimiento, '%Y-%m-%d'), DATE(NOW())), ' días')
            WHEN TIMESTAMPDIFF(MONTH, STR_TO_DATE(niños.fechaNacimiento, '%Y-%m-%d'), DATE(NOW())) < 12 THEN
                CONCAT(TIMESTAMPDIFF(MONTH, STR_TO_DATE(niños.fechaNacimiento, '%Y-%m-%d'), DATE(NOW())), ' meses')
            ELSE
                CONCAT(TIMESTAMPDIFF(YEAR, STR_TO_DATE(niños.fechaNacimiento, '%Y-%m-%d'), DATE(NOW())), ' años, ',
                        TIMESTAMPDIFF(MONTH, STR_TO_DATE(niños.fechaNacimiento, '%Y-%m-%d'), DATE(NOW())) % 12, ' meses, ',
                        FLOOR(TIMESTAMPDIFF(DAY, STR_TO_DATE(niños.fechaNacimiento, '%Y-%m-%d'), DATE(NOW())) % 30.436875), ' días')
        END AS edad
FROM niños
JOIN sexo ON niños.sexo = sexo.idSexo
JOIN establecimiento ON niños.idEstablecimiento = establecimiento.idEstablecimiento;

                   """)
    rows_padron = cursor.fetchall()
    cursor.close()
    database.close()

# Convertir resultados a JSONemo_json]})
    # Convertir resultados a JSON
    padron_json = []
    for row in rows_padron:
        dic = {}
        dic['num']= row[0]
        dic['dni']= row[1]
        dic['nombre']= row[2]
        dic['apPaterno']= row[3]
        dic['apMaterno']= row[4]
        dic['fechaNacimiento']= row[5]
        dic['programaSocial']= row[7]
        dic['sexo_descripcion']= row[9]
        dic['establecimiento_descripcion']= row[10]
        dic['edad']= row[11]
        padron_json.append(dic)

    return jsonify({"datos":[padron_json]})

def eliminar_tabla_reporte():
    try:
        database = get_database_connection()
        cursor = database.cursor()

        # Ejecuta el DELETE y resetea el AUTO_INCREMENT
        cursor.execute("DELETE FROM reportehemoglobina")
        cursor.execute("ALTER TABLE reportehemoglobina AUTO_INCREMENT = 1")

        # Confirma los cambios
        database.commit()

    except Error as e:
        print(f"Error al conectar con MySQL: {e}")

    finally:
        if cursor:
            cursor.close()
        if database:
            database.close()

def eliminar_tabla_niños():
    try:
        database = get_database_connection()
        cursor = database.cursor()

        # Ejecuta el DELETE y resetea el AUTO_INCREMENT
        cursor.execute("DELETE FROM niños")
        cursor.execute("ALTER TABLE niños AUTO_INCREMENT = 1")

        # Confirma los cambios
        database.commit()

    except Error as e:
        print(f"Error al conectar con MySQL: {e}")

    finally:
        if cursor:
            cursor.close()
        if database:
            database.close()

def eliminar_tabla_reporte():
    try:
        database = get_database_connection()
        cursor = database.cursor()

        # Ejecuta el DELETE y resetea el AUTO_INCREMENT
        cursor.execute("DELETE FROM reportehemoglobina")

        # Confirma los cambios
        database.commit()

    except Error as e:
        print(f"Error al conectar con MySQL: {e}")

    finally:
        if cursor:
            cursor.close()
        if database:
            database.close()