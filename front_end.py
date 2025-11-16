import os
import subprocess
import sys


def main() -> None:
    file_path = os.path.dirname(os.path.abspath(__file__))
    streamlit_path = os.path.join(file_path, "concept_filing.py")

    try:
        subprocess.run(
            [sys.executable, "-m", "streamlit", "run", streamlit_path],
            check=True,
        )
    except Exception as e:
        print(f"❌ Error al ejecutar Streamlit: {e}")


if __name__ == "__main__":
    main()
