import os
import psycopg2
import configparser
import logging
from datetime import datetime, timedelta
import csv

# Configuración de logging
log_dir = "logscript"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Generar el nombre del archivo de log basado en la fecha actual
log_filename = datetime.now().strftime('%Y-%m-%d.log')
log_filepath = os.path.join(log_dir, log_filename)

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler(log_filepath),
        logging.StreamHandler()  # Agregar manejador de consola
    ]
)

def clean_old_logs(log_directory, days_to_keep=15):
    """ Elimina archivos de log más antiguos que el número especificado de días. """
    today = datetime.now()
    cutoff_date = today - timedelta(days_to_keep)
    files_removed = 0

    for filename in os.listdir(log_directory):
        file_path = os.path.join(log_directory, filename)
        file_date_str = filename.split('.')[0]
        try:
            file_date = datetime.strptime(file_date_str, "%Y-%m-%d")
            if file_date < cutoff_date:
                os.remove(file_path)
                files_removed += 1
                logging.info(f"Archivo de log antiguo eliminado: {filename}")
        except ValueError:
            logging.info(f"No se pudo analizar la fecha del archivo: {filename}")

    logging.info(f"Total de archivos de log limpiados: {files_removed}")

# Llamar a la función para eliminar logs antiguos
clean_old_logs(log_dir)

# Leer configuración desde config.ini
config = configparser.RawConfigParser()
config.read('config.ini')

# Datos de conexión desde el archivo config.ini
db_host = config['DEFAULT']['db_host']
db_port = config['DEFAULT']['db_port']
db_user = config['DEFAULT']['db_user']
db_password = config['DEFAULT']['db_password']
db_name = config['DEFAULT']['db_name']
directorio_local = config['DEFAULT']['directorio_local']

def obtener_columnas_tabla(schema, table_name, connection):
    query = f"""
    SELECT column_name
    FROM information_schema.columns
    WHERE table_schema = '{schema}' AND table_name = '{table_name}'
    """
    cursor = connection.cursor()
    cursor.execute(query)
    columns = cursor.fetchall()
    cursor.close()
    # Omitir las columnas FECHA_CARGA y FECHA_ACTUALIZACION
    return [col[0].upper() for col in columns if col[0].upper() not in ['FECHA_CARGA', 'FECHA_ACTUALIZACION']]

def detect_delimiter(file_path):
    with open(file_path, 'r') as csvfile:
        sample = csvfile.read(1024)
        sniffer = csv.Sniffer()
        try:
            dialect = sniffer.sniff(sample)
            return dialect.delimiter
        except csv.Error:
            # Fallback to manual delimiter detection
            delimiters = [',', ';', '\t', '|', ' ']
            for delimiter in delimiters:
                if delimiter in sample:
                    return delimiter
            raise ValueError("Could not determine delimiter")

def cargar_csv_a_postgres(file_path, schema, table_name):
    max_retries = 3
    attempt = 0
    success = False

    try:
        delimiter = detect_delimiter(file_path)
    except ValueError as e:
        logging.error(f"Error al detectar el delimitador del archivo {file_path}: {e}")
        return

    while attempt < max_retries and not success:
        try:
            # Conexión a la base de datos
            connection = psycopg2.connect(
                host=db_host,
                port=db_port,
                user=db_user,
                password=db_password,
                dbname=db_name
            )
            
            # Obtener las columnas de la tabla
            columnas_tabla = obtener_columnas_tabla(schema, table_name, connection)
            
            # Leer el archivo CSV y preparar el contenido para COPY
            with open(file_path, 'r') as f:
                next(f)  # Saltar la fila de encabezado
                copy_sql = f"""
                COPY "{schema}"."{table_name}" ({', '.join(f'"{col}"' for col in columnas_tabla)}) 
                FROM STDIN WITH CSV HEADER
                DELIMITER AS '{delimiter}'
                """
                cursor = connection.cursor()
                cursor.copy_expert(sql=copy_sql, file=f)
                connection.commit()
                cursor.close()
                connection.close()
                logging.info(f"Datos cargados en {schema}.{table_name} desde {file_path}")
                success = True
        except Exception as e:
            attempt += 1
            logging.error(f"Error al cargar datos desde {file_path} a {schema}.{table_name}: {e}")
            if attempt < max_retries:
                logging.info(f"Reintentando cargar el archivo {file_path} ({attempt}/{max_retries})")
            else:
                logging.error(f"Máximo número de intentos alcanzado para el archivo {file_path}")
            if connection:
                connection.close()

def procesar_archivos_en_directorio(directorio_base):
    for root, dirs, files in os.walk(directorio_base):
        # Omitir el directorio base y procesar solo subdirectorios
        if root == directorio_base:
            continue
        for filename in files:
            if filename.endswith(".csv"):
                try:
                    # Extraer el esquema y el nombre de la tabla del nombre del archivo
                    schema, table_part = filename.split('-')
                    table_name = '_'.join(table_part.rsplit('_', 1)[:-1])
                    # Ruta completa del archivo
                    file_path = os.path.join(root, filename)

                    # Intentar cargar los datos del archivo CSV en la tabla correspondiente
                    cargar_csv_a_postgres(file_path, schema, table_name)
                except Exception as e:
                    logging.error(f"Error al procesar el archivo {filename}: {e}")

try:
    # Procesar todos los archivos en los subdirectorios del directorio local
    procesar_archivos_en_directorio(directorio_local)

except Exception as error:
    logging.error(f"Error al conectar a la base de datos o cargar los datos: {error}")
