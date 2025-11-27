import streamlit as st
import sqlite3
import pandas as pd
import os

def get_db_path():
    file_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.abspath(os.path.join(file_path, ".."))
    return os.path.join(file_path, "app_tecnoplus.db")

def administracion_usuarios():
    st.header("Administración de Usuarios")
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    
    # View Usuarios
    st.subheader("Ver Usuarios")
    usuarios_df = pd.read_sql_query("SELECT * FROM Usuarios", conn)
    st.dataframe(usuarios_df)
    
    # View Carrito
    st.subheader("Ver Carrito")
    carrito_df = pd.read_sql_query("SELECT * FROM Carrito", conn)
    st.dataframe(carrito_df)
    
    # Add Usuario
    st.subheader("Agregar Usuario")
    with st.form("add_usuario"):
        nombre = st.text_input("Nombre")
        correo_electronico = st.text_input("Correo Electrónico")
        contraseña = st.text_input("Contraseña", type="password")
        telefono = st.text_input("Teléfono")
        direccion = st.text_area("Dirección")
        rol = st.number_input("Rol", min_value=0, step=1)
        submitted = st.form_submit_button("Agregar")
        if submitted:
            try:
                conn.execute("""
                    INSERT INTO Usuarios (nombre, correo_electronico, contraseña, telefono, direccion, rol)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (nombre, correo_electronico, contraseña, telefono, direccion, rol))
                conn.commit()
                st.success("Usuario agregado")
            except Exception as e:
                st.error(f"Error: {e}")
    
    # Modify Usuario
    st.subheader("Modificar Usuario")
    usuario_ids = usuarios_df['id_usuario'].tolist()
    selected_id = st.selectbox("Seleccionar ID de Usuario", usuario_ids)
    if selected_id:
        user_data = usuarios_df[usuarios_df['id_usuario'] == selected_id].iloc[0]
        with st.form("modify_usuario"):
            nombre = st.text_input("Nombre", value=user_data['nombre'])
            correo_electronico = st.text_input("Correo Electrónico", value=user_data['correo_electronico'])
            contraseña = st.text_input("Contraseña", type="password", value=user_data['contraseña'])
            telefono = st.text_input("Teléfono", value=user_data['telefono'])
            direccion = st.text_area("Dirección", value=user_data['direccion'])
            rol = st.number_input("Rol", min_value=0, step=1, value=user_data['rol'])
            estado = st.checkbox("Estado", value=bool(user_data['estado']))
            submitted = st.form_submit_button("Modificar")
            if submitted:
                try:
                    conn.execute("""
                        UPDATE Usuarios SET nombre=?, correo_electronico=?, contraseña=?, telefono=?, direccion=?, rol=?, estado=?
                        WHERE id_usuario=?
                    """, (nombre, correo_electronico, contraseña, telefono, direccion, rol, int(estado), selected_id))
                    conn.commit()
                    st.success("Usuario modificado")
                except Exception as e:
                    st.error(f"Error: {e}")
    
    # Delete Usuario
    st.subheader("Eliminar Usuario")
    delete_id = st.selectbox("Seleccionar ID para Eliminar", usuario_ids, key="delete")
    if st.button("Eliminar"):
        try:
            conn.execute("DELETE FROM Usuarios WHERE id_usuario=?", (delete_id,))
            conn.commit()
            st.success("Usuario eliminado")
        except Exception as e:
            st.error(f"Error: {e}")
    
    conn.close()

def administracion_productos():
    st.header("Administración de Productos")
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    
    # Categorias
    st.subheader("Categorías")
    categorias_df = pd.read_sql_query("SELECT * FROM Categorias", conn)
    st.dataframe(categorias_df)
    
    with st.expander("Agregar/Modificar Categoría"):
        action = st.radio("Acción", ["Agregar", "Modificar"])
        if action == "Agregar":
            with st.form("add_categoria"):
                nombre = st.text_input("Nombre")
                descripcion = st.text_area("Descripción")
                submitted = st.form_submit_button("Agregar")
                if submitted:
                    try:
                        conn.execute("INSERT INTO Categorias (nombre, descripcion) VALUES (?, ?)", (nombre, descripcion))
                        conn.commit()
                        st.success("Categoría agregada")
                    except Exception as e:
                        st.error(f"Error: {e}")
        else:
            cat_ids = categorias_df['id_categoria'].tolist()
            selected_id = st.selectbox("Seleccionar ID", cat_ids)
            if selected_id:
                cat_data = categorias_df[categorias_df['id_categoria'] == selected_id].iloc[0]
                with st.form("modify_categoria"):
                    nombre = st.text_input("Nombre", value=cat_data['nombre'])
                    descripcion = st.text_area("Descripción", value=cat_data['descripcion'])
                    estado = st.checkbox("Estado", value=bool(cat_data['estado']))
                    submitted = st.form_submit_button("Modificar")
                    if submitted:
                        try:
                            conn.execute("UPDATE Categorias SET nombre=?, descripcion=?, estado=? WHERE id_categoria=?", (nombre, descripcion, int(estado), selected_id))
                            conn.commit()
                            st.success("Categoría modificada")
                        except Exception as e:
                            st.error(f"Error: {e}")
    
    # Productos
    st.subheader("Productos")
    productos_df = pd.read_sql_query("SELECT * FROM Productos", conn)
    st.dataframe(productos_df)
    
    with st.expander("Agregar/Modificar Producto"):
        action = st.radio("Acción", ["Agregar", "Modificar"], key="prod")
        if action == "Agregar":
            with st.form("add_producto"):
                nombre = st.text_input("Nombre")
                descripcion = st.text_area("Descripción")
                id_categoria = st.number_input("ID Categoría", min_value=1, step=1)
                id_marca = st.number_input("ID Marca", min_value=1, step=1)
                precio = st.number_input("Precio", min_value=0.0, step=0.01)
                stock = st.number_input("Stock", min_value=0, step=1)
                imagen_url = st.text_input("Imagen URL")
                submitted = st.form_submit_button("Agregar")
                if submitted:
                    try:
                        conn.execute("""
                            INSERT INTO Productos (nombre, descripcion, id_categoria, id_marca, precio, stock, imagen_url)
                            VALUES (?, ?, ?, ?, ?, ?, ?)
                        """, (nombre, descripcion, id_categoria, id_marca, precio, stock, imagen_url))
                        conn.commit()
                        st.success("Producto agregado")
                    except Exception as e:
                        st.error(f"Error: {e}")
        else:
            prod_ids = productos_df['id_producto'].tolist()
            selected_id = st.selectbox("Seleccionar ID", prod_ids, key="prod_sel")
            if selected_id:
                prod_data = productos_df[productos_df['id_producto'] == selected_id].iloc[0]
                with st.form("modify_producto"):
                    nombre = st.text_input("Nombre", value=prod_data['nombre'])
                    descripcion = st.text_area("Descripción", value=prod_data['descripcion'])
                    id_categoria = st.number_input("ID Categoría", min_value=1, step=1, value=prod_data['id_categoria'])
                    id_marca = st.number_input("ID Marca", min_value=1, step=1, value=prod_data['id_marca'])
                    precio = st.number_input("Precio", min_value=0.0, step=0.01, value=prod_data['precio'])
                    stock = st.number_input("Stock", min_value=0, step=1, value=prod_data['stock'])
                    imagen_url = st.text_input("Imagen URL", value=prod_data['imagen_url'])
                    estado = st.checkbox("Estado", value=bool(prod_data['estado']))
                    submitted = st.form_submit_button("Modificar")
                    if submitted:
                        try:
                            conn.execute("""
                                UPDATE Productos SET nombre=?, descripcion=?, id_categoria=?, id_marca=?, precio=?, stock=?, imagen_url=?, estado=?
                                WHERE id_producto=?
                            """, (nombre, descripcion, id_categoria, id_marca, precio, stock, imagen_url, int(estado), selected_id))
                            conn.commit()
                            st.success("Producto modificado")
                        except Exception as e:
                            st.error(f"Error: {e}")
    
    # Inventario
    st.subheader("Inventario")
    inventario_df = pd.read_sql_query("SELECT * FROM Inventario", conn)
    st.dataframe(inventario_df)
    
    with st.expander("Agregar/Modificar Inventario"):
        action = st.radio("Acción", ["Agregar", "Modificar"], key="inv")
        if action == "Agregar":
            with st.form("add_inventario"):
                id_producto = st.number_input("ID Producto", min_value=1, step=1)
                tipo_movimiento = st.selectbox("Tipo Movimiento", ["entrada", "salida", "ajuste", "devolución"])
                cantidad = st.number_input("Cantidad", step=1)
                motivo = st.text_area("Motivo")
                usuario_responsable = st.number_input("Usuario Responsable", min_value=1, step=1)
                submitted = st.form_submit_button("Agregar")
                if submitted:
                    try:
                        conn.execute("""
                            INSERT INTO Inventario (id_producto, tipo_movimiento, cantidad, motivo, usuario_responsable)
                            VALUES (?, ?, ?, ?, ?)
                        """, (id_producto, tipo_movimiento, cantidad, motivo, usuario_responsable))
                        conn.commit()
                        st.success("Movimiento agregado")
                    except Exception as e:
                        st.error(f"Error: {e}")
        else:
            inv_ids = inventario_df['id_movimiento'].tolist()
            selected_id = st.selectbox("Seleccionar ID", inv_ids, key="inv_sel")
            if selected_id:
                inv_data = inventario_df[inventario_df['id_movimiento'] == selected_id].iloc[0]
                with st.form("modify_inventario"):
                    id_producto = st.number_input("ID Producto", min_value=1, step=1, value=inv_data['id_producto'])
                    tipo_movimiento = st.selectbox("Tipo Movimiento", ["entrada", "salida", "ajuste", "devolución"], index=["entrada", "salida", "ajuste", "devolución"].index(inv_data['tipo_movimiento']))
                    cantidad = st.number_input("Cantidad", step=1, value=inv_data['cantidad'])
                    motivo = st.text_area("Motivo", value=inv_data['motivo'])
                    usuario_responsable = st.number_input("Usuario Responsable", min_value=1, step=1, value=inv_data['usuario_responsable'])
                    submitted = st.form_submit_button("Modificar")
                    if submitted:
                        try:
                            conn.execute("""
                                UPDATE Inventario SET id_producto=?, tipo_movimiento=?, cantidad=?, motivo=?, usuario_responsable=?
                                WHERE id_movimiento=?
                            """, (id_producto, tipo_movimiento, cantidad, motivo, usuario_responsable, selected_id))
                            conn.commit()
                            st.success("Movimiento modificado")
                        except Exception as e:
                            st.error(f"Error: {e}")
    
    # Reseñas
    st.subheader("Reseñas")
    reseñas_df = pd.read_sql_query("SELECT * FROM Reseñas", conn)
    st.dataframe(reseñas_df)
    
    with st.expander("Agregar/Modificar Reseña"):
        action = st.radio("Acción", ["Agregar", "Modificar"], key="res")
        if action == "Agregar":
            with st.form("add_reseña"):
                id_usuario = st.number_input("ID Usuario", min_value=1, step=1)
                id_producto = st.number_input("ID Producto", min_value=1, step=1)
                calificacion = st.slider("Calificación", 1, 5)
                comentario = st.text_area("Comentario")
                submitted = st.form_submit_button("Agregar")
                if submitted:
                    try:
                        conn.execute("""
                            INSERT INTO Reseñas (id_usuario, id_producto, calificacion, comentario)
                            VALUES (?, ?, ?, ?)
                        """, (id_usuario, id_producto, calificacion, comentario))
                        conn.commit()
                        st.success("Reseña agregada")
                    except Exception as e:
                        st.error(f"Error: {e}")
        else:
            res_ids = reseñas_df['id_reseña'].tolist()
            selected_id = st.selectbox("Seleccionar ID", res_ids, key="res_sel")
            if selected_id:
                res_data = reseñas_df[reseñas_df['id_reseña'] == selected_id].iloc[0]
                with st.form("modify_reseña"):
                    id_usuario = st.number_input("ID Usuario", min_value=1, step=1, value=res_data['id_usuario'])
                    id_producto = st.number_input("ID Producto", min_value=1, step=1, value=res_data['id_producto'])
                    calificacion = st.slider("Calificación", 1, 5, value=res_data['calificacion'])
                    comentario = st.text_area("Comentario", value=res_data['comentario'])
                    estado = st.checkbox("Estado", value=bool(res_data['estado']))
                    submitted = st.form_submit_button("Modificar")
                    if submitted:
                        try:
                            conn.execute("""
                                UPDATE Reseñas SET id_usuario=?, id_producto=?, calificacion=?, comentario=?, estado=?
                                WHERE id_reseña=?
                            """, (id_usuario, id_producto, calificacion, comentario, int(estado), selected_id))
                            conn.commit()
                            st.success("Reseña modificada")
                        except Exception as e:
                            st.error(f"Error: {e}")
    
    conn.close()

def generacion_pedido():
    import streamlit as st
    import pandas as pd
    import sqlite3
    from datetime import datetime
    import uuid

    st.header("🛒 Generación de Pedido")

    db_path = get_db_path()  # asumes que ya existe en tu app
    conn = sqlite3.connect(db_path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    try:
        # Cargar usuarios
        users_df = pd.read_sql_query("SELECT id_usuario, nombre FROM Usuarios ORDER BY nombre;", conn)
        if users_df.empty:
            st.warning("No hay usuarios registrados. Ve a 'Administración de usuarios' primero.")
            conn.close()
            return

        user_map = {row["nombre"]: int(row["id_usuario"]) for _, row in users_df.iterrows()}
        usuario_seleccionado_nombre = st.selectbox("Selecciona usuario:", list(user_map.keys()))
        id_usuario = user_map[usuario_seleccionado_nombre]

        st.markdown("---")
        st.subheader("Productos disponibles")
        productos_df = pd.read_sql_query(
            "SELECT id_producto, nombre, descripcion, precio, stock FROM Productos WHERE estado=1 ORDER BY nombre;",
            conn
        )
        if productos_df.empty:
            st.info("No hay productos activos.")
        else:
            st.dataframe(productos_df[["id_producto", "nombre", "precio", "stock"]], use_container_width=True)

            # Agregar al carrito: elegir producto y cantidad
            col1, col2, col3 = st.columns([4,1,1])
            with col1:
                opciones_prod = {f"{r['nombre']} (stock:{int(r['stock'])})": int(r['id_producto']) for _, r in productos_df.iterrows()}
                seleccion_prod_display = st.selectbox("Seleccionar producto a agregar:", ["---"] + list(opciones_prod.keys()))
            with col2:
                cantidad = st.number_input("Cantidad", min_value=1, step=1, value=1)
            with col3:
                if st.button("➕ Agregar al carrito"):
                    if seleccion_prod_display == "---":
                        st.error("Selecciona un producto válido.")
                    else:
                        id_producto = opciones_prod[seleccion_prod_display]
                        # comprobar stock
                        cur.execute("SELECT stock, nombre FROM Productos WHERE id_producto = ?;", (id_producto,))
                        prod_row = cur.fetchone()
                        if not prod_row:
                            st.error("Producto no encontrado.")
                        else:
                            stock = int(prod_row["stock"])
                            nombre_prod = prod_row["nombre"]
                            if cantidad > stock:
                                st.error(f"No hay stock suficiente para '{nombre_prod}' (stock={stock}).")
                            else:
                                # insertar o actualizar en Carrito (si existe, actualizamos la cantidad sumando)
                                # Primero revisar si ya existe fila para ese usuario/producto
                                cur.execute("SELECT id_carrito, cantidad FROM Carrito WHERE id_usuario = ? AND id_producto = ?;",
                                            (id_usuario, id_producto))
                                existing = cur.fetchone()
                                if existing:
                                    nueva_cant = int(existing["cantidad"]) + int(cantidad)
                                    if nueva_cant > stock:
                                        st.error(f"No puedes tener más de {stock} unidades de '{nombre_prod}' en carrito.")
                                    else:
                                        cur.execute("UPDATE Carrito SET cantidad = ?, fecha_agregado = DATETIME('now') WHERE id_carrito = ?;",
                                                    (nueva_cant, existing["id_carrito"]))
                                        conn.commit()
                                        st.success(f"Cantidad actualizada en carrito: {nueva_cant} de '{nombre_prod}'.")
                                else:
                                    cur.execute("INSERT INTO Carrito (id_usuario, id_producto, cantidad, fecha_agregado) VALUES (?, ?, ?, DATETIME('now'));",
                                                (id_usuario, id_producto, int(cantidad)))
                                    conn.commit()
                                    st.success(f"'{nombre_prod}' agregado al carrito ({cantidad}).")

        st.markdown("---")
        st.subheader("Carrito")
        carrito_df = pd.read_sql_query(
            "SELECT c.id_carrito, c.id_producto, p.nombre, p.precio, c.cantidad, p.stock "
            "FROM Carrito c JOIN Productos p ON c.id_producto = p.id_producto "
            "WHERE c.id_usuario = ? ORDER BY c.fecha_agregado;",
            conn, params=(id_usuario,)
        )

        if carrito_df.empty:
            st.info("El carrito está vacío.")
        else:
            # Mostrar items y permitir edición/eliminación
            st.write("Edita cantidades y pulsa 'Actualizar' o elimina elementos individualmente.")
            cambios = {}
            for idx, r in carrito_df.iterrows():
                id_carrito = int(r["id_carrito"])
                nombre = r["nombre"]
                precio = float(r["precio"])
                cantidad_actual = int(r["cantidad"])
                stock = int(r["stock"])

                cols = st.columns([4,1,1])
                cols[0].markdown(f"**{nombre}** — ${precio:.2f} — stock: {stock}")
                nueva_q = cols[1].number_input("Cantidad", min_value=0, max_value=stock, value=cantidad_actual, key=f"qty_{id_carrito}")
                if nueva_q != cantidad_actual:
                    cambios[id_carrito] = int(nueva_q)
                if cols[2].button("Eliminar", key=f"del_{id_carrito}"):
                    cur.execute("DELETE FROM Carrito WHERE id_carrito = ?;", (id_carrito,))
                    conn.commit()
                    st.experimental_rerun()

            if cambios:
                if st.button("Actualizar carrito"):
                    for id_carrito, q in cambios.items():
                        if q <= 0:
                            cur.execute("DELETE FROM Carrito WHERE id_carrito = ?;", (id_carrito,))
                        else:
                            # obtener id_producto y stock para validar
                            cur.execute("SELECT id_producto FROM Carrito WHERE id_carrito = ?;", (id_carrito,))
                            r = cur.fetchone()
                            if r:
                                id_prod = r["id_producto"]
                                cur.execute("SELECT stock FROM Productos WHERE id_producto = ?;", (id_prod,))
                                stock_r = cur.fetchone()
                                if stock_r and q > int(stock_r["stock"]):
                                    st.error(f"No hay stock suficiente para el producto (id {id_prod}). Se saltó actualización.")
                                else:
                                    cur.execute("UPDATE Carrito SET cantidad = ?, fecha_agregado = DATETIME('now') WHERE id_carrito = ?;", (q, id_carrito))
                    conn.commit()
                    st.success("Carrito actualizado.")
                    st.experimental_rerun()

            # Resumen y pago
            carrito_df["subtotal"] = carrito_df["precio"] * carrito_df["cantidad"]
            total = carrito_df["subtotal"].sum()
            st.markdown("---")
            st.write("### Resumen del carrito")
            st.dataframe(carrito_df[["nombre", "precio", "cantidad", "subtotal"]].rename(columns={
                "nombre":"Producto","precio":"Precio","cantidad":"Cantidad","subtotal":"Subtotal"
            }), use_container_width=True)
            st.markdown(f"**Total a pagar:** ${total:.2f}")

            metodo = st.radio("Método de pago:", ("tarjeta", "transferencia", "efectivo", "paypal"))
            marcar_aprobado = metodo in ("tarjeta", "paypal")  # lógica simple: tarjeta/paypal aprobados al instante

            if st.button("💳 Pagar ahora"):
                try:
                    res = generar_pago_desde_carrito(id_usuario, metodo)
                    st.success(f"Pago registrado (id_pago={res['id_pago']}) — estado: {res['estado_pago']} — referencia: {res['referencia']}")
                    st.write(f"- Monto: ${res['total']:.2f}")
                    st.experimental_rerun()
                except Exception as e:
                    st.error(f"Error al procesar el pago: {e}")

    except Exception as e_main:
        st.error(f"Error inesperado: {e_main}")
    finally:
        conn.close()


st.title("Administración de la Base de Datos")
vista = st.sidebar.selectbox("Seleccionar Vista", ["Administración de usuarios", "Administración de productos", "Generación de pedido"])

if vista == "Administración de usuarios":
    administracion_usuarios()
elif vista == "Administración de productos":
    administracion_productos()
elif vista == "Generación de pedido":
    generacion_pedido()
st.title("Administración de la Base de Datos")
vista = st.sidebar.selectbox("Seleccionar Vista", ["Administración de usuarios", "Administración de productos"])

if vista == "Administración de usuarios":
    administracion_usuarios()
elif vista == "Administración de productos":
    administracion_productos()



