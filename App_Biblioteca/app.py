from flask import Flask, render_template, request, send_file
import pyodbc
import pandas as pd
import os
from datetime import datetime

app = Flask(__name__)

# Configuración de la conexión a SQL Server con autenticación de Windows
DB_CONFIG = {
    'driver': '{ODBC Driver 17 for SQL Server}',
    'server': '',
    'database': '',
    'trusted_connection': ''
}

def get_db_connection():
    """Establece conexión con SQL Server."""
    conn = pyodbc.connect(
        f"DRIVER={DB_CONFIG['driver']};"
        f"SERVER={DB_CONFIG['server']};"
        f"DATABASE={DB_CONFIG['database']};"
        f"Trusted_Connection={DB_CONFIG['trusted_connection']};"
    )
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/buscar', methods=['GET'])
def buscar():
    titulo = request.args.get('titulo', '')
    autor = request.args.get('autor', '')
    genero = request.args.get('genero', '')

    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
        SELECT ID, Titulo, Autor, AnioPublicacion, Editorial, Genero, ISBN, Disponible
        FROM Libros
        WHERE Titulo LIKE ? AND Autor LIKE ? AND Genero LIKE ?
    """
    cursor.execute(query, (f'%{titulo}%', f'%{autor}%', f'%{genero}%'))
    libros = cursor.fetchall()
    conn.close()
    
    return {'libros': [dict(zip([column[0] for column in cursor.description], row)) for row in libros]}

@app.route('/exportar', methods=['POST'])
def exportar():
    fecha_inicio = request.form['fecha_inicio']
    fecha_fin = request.form['fecha_fin']
    conn = get_db_connection()
    query = """
        SELECT * FROM Registros
        WHERE FechaHoraPrestamo BETWEEN ? AND ?
    """
    df = pd.read_sql(query, conn, params=[fecha_inicio, fecha_fin])
    conn.close()
    
    file_path = os.path.join(os.getcwd(), f"registros_{datetime.now().strftime('%Y%m%d%H%M%S')}.xlsx")
    df.to_excel(file_path, index=False)
    
    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
