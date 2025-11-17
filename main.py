import os
import subprocess
import sys
from app_web.sql_init import inicializar_db

def main() -> None:

    
    file_path = os.path.dirname(os.path.abspath(__file__))
    streamlit_path = os.path.join(file_path, "app_web", "llenar_app.py")
    inicializar_db(file_path)
    try:
        subprocess.run(
            [sys.executable, "-m", "streamlit", "run", streamlit_path],
            check=True,
        )
    except Exception as e:
        print(f"❌ Error al ejecutar Streamlit: {e}")


if __name__ == "__main__":
    main()
