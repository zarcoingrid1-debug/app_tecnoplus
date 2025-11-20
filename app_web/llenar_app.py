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

st.title("Administración de la Base de Datos")
vista = st.sidebar.selectbox("Seleccionar Vista", ["Administración de usuarios", "Administración de productos"])

if vista == "Administración de usuarios":
    administracion_usuarios()
elif vista == "Administración de productos":
    administracion_productos()



