import csv
import os

import boto3
import mysql.connector


# Configuración de MySQL
MYSQL_HOST = "172.31.26.96"
MYSQL_PORT = 8005
MYSQL_USER = "root"
MYSQL_DATABASE = "bd_api_employees"

# La contraseña se recibe al ejecutar el programa.
MYSQL_PASSWORD = os.environ["MYSQL_PASSWORD"]

# Configuración de S3
nombreBucket = "santiago-ingesta02-2026"
REGION = "us-east-1"

# Archivo que generará el programa
nombreArchivo = "data.csv"


def main():
    print("1. Conectando con MySQL...", flush=True)

    conexion = mysql.connector.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE,
        connection_timeout=15
    )

    cursor = conexion.cursor()

    try:
        cursor.execute("SELECT * FROM employees ORDER BY id")

        registros = cursor.fetchall()
        columnas = [columna[0] for columna in cursor.description]

        print(
            f"2. Registros leídos de employees: {len(registros)}",
            flush=True
        )

        with open(
            nombreArchivo,
            "w",
            newline="",
            encoding="utf-8"
        ) as archivo:
            escritor = csv.writer(archivo)
            escritor.writerow(columnas)
            escritor.writerows(registros)

        print(f"3. Archivo CSV generado: {nombreArchivo}", flush=True)

    finally:
        cursor.close()
        conexion.close()

    s3 = boto3.client("s3", region_name=REGION)

    s3.upload_file(
        nombreArchivo,
        nombreBucket,
        nombreArchivo
    )

    print(
        f"4. Archivo subido a s3://{nombreBucket}/{nombreArchivo}",
        flush=True
    )

    print("Ingesta completada", flush=True)


if __name__ == "__main__":
    main()
