
import os
import sqlite3

def inicializar_db(file_path):
    # Ubicación del archivo SQL base
    sql_start_archivo = os.path.join(file_path, "sql", "sql_init.sql")
    print(sql_start_archivo)
    db_path = os.path.join(file_path, "app_tecnoplus.db")
    if not os.path.exists(db_path):
        # Crear la base de datos SQLite y ejecutar el esquema desde sql_init.sql
        conn = sqlite3.connect(db_path)
        with open(sql_start_archivo, 'r', encoding='utf-8') as f:
            sql_script = f.read()
        conn.executescript(sql_script)
        conn.close()
        print(f"Base de datos SQLite inicializada en: {db_path} conforme al esquema en {sql_start_archivo}")
    else:
        print(f"La base de datos ya existe en: {db_path}")


if __name__ == "__main__":
    file_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.abspath(os.path.join(file_path, ".."))
    inicializar_db(file_path)
    
