# app_tecnoplus Copilot Instructions

## Architecture Overview
This is a Python-based e-commerce application using Streamlit for the web interface and SQLite for data persistence. The app manages users, products, orders, payments, and inventory.

- **Main Entry**: `main.py` launches the Streamlit app by running `streamlit run concept_filing.py` (note: `concept_filing.py` is referenced but not present in the workspace).
- **Web Components**: `app_web/` directory contains web-related modules (currently `llenar_app.py` is empty, likely intended for data population).
- **Database Schema**: `sql/sql_init.sql` defines the SQLite schema with tables like `Usuarios`, `Productos`, `Pedidos`, etc., using Spanish naming conventions.

## Key Patterns
- **Database**: Uses SQLite with foreign keys and generated columns (e.g., `subtotal` in `Detalle_Pedido`).
- **Naming**: Table and column names in Spanish (e.g., `id_usuario`, `nombre`, `fecha_registro`).
- **State Management**: Relies on Streamlit's session state for user interactions.
- **Error Handling**: Basic try-except in `main.py` for subprocess execution.

## Workflows
- **Run App**: Execute `python main.py` from the project root (activates conda env `personal_conda`).
- **Database Setup**: Run `sql/sql_init.sql` in SQLite to initialize schema.
- **Data Population**: Implement logic in `app_web/llenar_app.py` to insert sample data into tables.

## Dependencies
- **Python Packages**: `streamlit` (installed in conda env).
- **Database**: SQLite (built-in with Python).

## Conventions
- **Imports**: Relative imports for modules (e.g., `from app_web.llenar_app`).
- **File Structure**: Separate directories for web (`app_web/`) and database (`sql/`).
- **SQL**: Uses `IF NOT EXISTS` for safe table creation, CHECK constraints for enums.

Reference: `sql/sql_init.sql` for schema examples, `main.py` for app launch pattern.