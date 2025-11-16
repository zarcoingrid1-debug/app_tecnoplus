import streamlit as st


def render_home_view() -> None:
    """First view: welcome message plus user input."""
    st.title("Panel principal")
    st.write(
        "Bienvenido a la aplicacion demo de Tecnoplus. "
        "Completa el formulario para generar un resumen personalizado."
    )

    nombre = st.text_input("Tu nombre")
    proyecto = st.text_input("Nombre del proyecto", value="Migracion a la nube")
    nivel_confianza = st.slider("Nivel de confianza", 0, 100, 80)

    if st.button("Generar saludo"):
        st.success(
            f"Hola {nombre or 'equipo'}, estas trabajando en {proyecto} "
            f"con un nivel de confianza del {nivel_confianza}%."
        )


def render_report_view() -> None:
    """Second view: simple metrics and data table."""
    st.title("Vista de reportes")
    st.caption("Resumen semanal de KPIs.")

    col1, col2, col3 = st.columns(3)
    col1.metric("Nuevos clientes", "32", "+5")
    col2.metric("Tickets resueltos", "128", "+12")
    col3.metric("Satisfaccion", "94%", "+2%")

    st.write("Detalle por ejecutivo")
    st.table(
        {
            "Ejecutivo": ["Ana", "Luis", "Carla", "Pedro"],
            "Clientes": [12, 8, 6, 6],
            "Tickets": [45, 32, 29, 22],
        }
    )


def main() -> None:
    st.set_page_config(page_title="Tecnoplus", layout="wide")
    st.sidebar.title("Navegacion")
    vista = st.sidebar.radio(
        "Selecciona una vista",
        (
            "Panel principal",
            "Reportes",
        ),
    )

    if vista == "Panel principal":
        render_home_view()
    else:
        render_report_view()


if __name__ == "__main__":
    main()
