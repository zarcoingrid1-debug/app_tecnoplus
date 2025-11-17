import streamlit as st
import sqlite3
import os


def get_db_path():
    file_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.abspath(os.path.join(file_path, ".."))
    return os.path.join(file_path, "app_tecnoplus.db")


def insert_usuario(conn, nombre, correo_electronico, contraseña, telefono, direccion, rol):
    conn.execute("""
        INSERT INTO Usuarios (nombre, correo_electronico, contraseña, telefono, direccion, rol)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (nombre, correo_electronico, contraseña, telefono, direccion, rol))
    conn.commit()


def insert_producto(conn, nombre, descripcion, id_categoria, id_marca, precio, stock, imagen_url):
    conn.execute("""
        INSERT INTO Productos (nombre, descripcion, id_categoria, id_marca, precio, stock, imagen_url)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (nombre, descripcion, id_categoria, id_marca, precio, stock, imagen_url))
    conn.commit()


def insert_categoria(conn, nombre, descripcion):
    conn.execute("""
        INSERT INTO Categorias (nombre, descripcion)
        VALUES (?, ?)
    """, (nombre, descripcion))
    conn.commit()


def insert_pedido(conn, id_usuario, total, estado, observaciones, direccion_envio):
    conn.execute("""
        INSERT INTO Pedidos (id_usuario, total, estado, observaciones, direccion_envio)
        VALUES (?, ?, ?, ?, ?)
    """, (id_usuario, total, estado, observaciones, direccion_envio))
    conn.commit()


def insert_detalle_pedido(conn, id_pedido, id_producto, cantidad, precio_unitario):
    conn.execute("""
        INSERT INTO Detalle_Pedido (id_pedido, id_producto, cantidad, precio_unitario)
        VALUES (?, ?, ?, ?)
    """, (id_pedido, id_producto, cantidad, precio_unitario))
    conn.commit()


def insert_carrito(conn, id_usuario, id_producto, cantidad):
    conn.execute("""
        INSERT INTO Carrito (id_usuario, id_producto, cantidad)
        VALUES (?, ?, ?)
    """, (id_usuario, id_producto, cantidad))
    conn.commit()


def insert_pago(conn, id_pedido, monto_pagado, metodo_pago, estado_pago, referencia_transaccion):
    conn.execute("""
        INSERT INTO Pagos (id_pedido, monto_pagado, metodo_pago, estado_pago, referencia_transaccion)
        VALUES (?, ?, ?, ?, ?)
    """, (id_pedido, monto_pagado, metodo_pago, estado_pago, referencia_transaccion))
    conn.commit()


def insert_envio(conn, id_pedido, empresa_envio, numero_guia, fecha_entrega_estimada, estado_envio, direccion_entrega, observaciones):
    conn.execute("""
        INSERT INTO Envios (id_pedido, empresa_envio, numero_guia, fecha_entrega_estimada, estado_envio, direccion_entrega, observaciones)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (id_pedido, empresa_envio, numero_guia, fecha_entrega_estimada, estado_envio, direccion_entrega, observaciones))
    conn.commit()


def insert_reseña(conn, id_usuario, id_producto, calificacion, comentario):
    conn.execute("""
        INSERT INTO Reseñas (id_usuario, id_producto, calificacion, comentario)
        VALUES (?, ?, ?, ?)
    """, (id_usuario, id_producto, calificacion, comentario))
    conn.commit()


def insert_inventario(conn, id_producto, tipo_movimiento, cantidad, motivo, usuario_responsable):
    conn.execute("""
        INSERT INTO Inventario (id_producto, tipo_movimiento, cantidad, motivo, usuario_responsable)
        VALUES (?, ?, ?, ?, ?)
    """, (id_producto, tipo_movimiento, cantidad, motivo, usuario_responsable))
    conn.commit()


def insert_historial_acceso(conn, id_usuario, accion_realizada, ip_usuario, navegador):
    conn.execute("""
        INSERT INTO Historial_Acceso (id_usuario, accion_realizada, ip_usuario, navegador)
        VALUES (?, ?, ?, ?)
    """, (id_usuario, accion_realizada, ip_usuario, navegador))
    conn.commit()


st.title("App Tecnoplus UNITEC IYP")

db_path = get_db_path()
conn = sqlite3.connect(db_path)

tab_usuarios, tab_productos, tab_categorias, tab_pedidos, tab_detalle_pedido, tab_carrito, tab_pagos, tab_envios, tab_reseñas, tab_inventario, tab_historial = st.tabs([
    "Usuarios", "Productos", "Categorias", "Pedidos", "Detalle_Pedido", "Carrito", "Pagos", "Envios", "Reseñas", "Inventario", "Historial_Acceso"
])

with tab_usuarios:
    st.header("Agregar Usuario")
    with st.form("usuario_form"):
        nombre = st.text_input("Nombre")
        correo_electronico = st.text_input("Correo Electrónico")
        contraseña = st.text_input("Contraseña", type="password")
        telefono = st.text_input("Teléfono")
        direccion = st.text_area("Dirección")
        rol = st.number_input("Rol", min_value=0, step=1)
        submitted = st.form_submit_button("Agregar Usuario")
        if submitted:
            insert_usuario(conn, nombre, correo_electronico, contraseña, telefono, direccion, rol)
            st.success("Usuario agregado exitosamente")

with tab_productos:
    st.header("Agregar Producto")
    with st.form("producto_form"):
        nombre = st.text_input("Nombre")
        descripcion = st.text_area("Descripción")
        id_categoria = st.number_input("ID Categoría", min_value=1, step=1)
        id_marca = st.number_input("ID Marca", min_value=1, step=1)  # Assuming Marcas table exists or add later
        precio = st.number_input("Precio", min_value=0.0, step=0.01)
        stock = st.number_input("Stock", min_value=0, step=1)
        imagen_url = st.text_input("Imagen URL")
        submitted = st.form_submit_button("Agregar Producto")
        if submitted:
            insert_producto(conn, nombre, descripcion, id_categoria, id_marca, precio, stock, imagen_url)
            st.success("Producto agregado exitosamente")

with tab_categorias:
    st.header("Agregar Categoría")
    with st.form("categoria_form"):
        nombre = st.text_input("Nombre")
        descripcion = st.text_area("Descripción")
        submitted = st.form_submit_button("Agregar Categoría")
        if submitted:
            insert_categoria(conn, nombre, descripcion)
            st.success("Categoría agregada exitosamente")

with tab_pedidos:
    st.header("Agregar Pedido")
    with st.form("pedido_form"):
        id_usuario = st.number_input("ID Usuario", min_value=1, step=1)
        total = st.number_input("Total", min_value=0.0, step=0.01)
        estado = st.selectbox("Estado", ["pendiente", "pagado", "enviado", "cancelado"])
        observaciones = st.text_area("Observaciones")
        direccion_envio = st.text_area("Dirección de Envío")
        submitted = st.form_submit_button("Agregar Pedido")
        if submitted:
            insert_pedido(conn, id_usuario, total, estado, observaciones, direccion_envio)
            st.success("Pedido agregado exitosamente")

with tab_detalle_pedido:
    st.header("Agregar Detalle de Pedido")
    with st.form("detalle_pedido_form"):
        id_pedido = st.number_input("ID Pedido", min_value=1, step=1)
        id_producto = st.number_input("ID Producto", min_value=1, step=1)
        cantidad = st.number_input("Cantidad", min_value=1, step=1)
        precio_unitario = st.number_input("Precio Unitario", min_value=0.0, step=0.01)
        submitted = st.form_submit_button("Agregar Detalle de Pedido")
        if submitted:
            insert_detalle_pedido(conn, id_pedido, id_producto, cantidad, precio_unitario)
            st.success("Detalle de Pedido agregado exitosamente")

with tab_carrito:
    st.header("Agregar al Carrito")
    with st.form("carrito_form"):
        id_usuario = st.number_input("ID Usuario", min_value=1, step=1)
        id_producto = st.number_input("ID Producto", min_value=1, step=1)
        cantidad = st.number_input("Cantidad", min_value=1, step=1)
        submitted = st.form_submit_button("Agregar al Carrito")
        if submitted:
            insert_carrito(conn, id_usuario, id_producto, cantidad)
            st.success("Agregado al carrito exitosamente")

with tab_pagos:
    st.header("Agregar Pago")
    with st.form("pago_form"):
        id_pedido = st.number_input("ID Pedido", min_value=1, step=1)
        monto_pagado = st.number_input("Monto Pagado", min_value=0.0, step=0.01)
        metodo_pago = st.selectbox("Método de Pago", ["tarjeta", "transferencia", "efectivo", "paypal"])
        estado_pago = st.selectbox("Estado de Pago", ["pendiente", "aprobado", "rechazado"])
        referencia_transaccion = st.text_input("Referencia de Transacción")
        submitted = st.form_submit_button("Agregar Pago")
        if submitted:
            insert_pago(conn, id_pedido, monto_pagado, metodo_pago, estado_pago, referencia_transaccion)
            st.success("Pago agregado exitosamente")

with tab_envios:
    st.header("Agregar Envío")
    with st.form("envio_form"):
        id_pedido = st.number_input("ID Pedido", min_value=1, step=1)
        empresa_envio = st.text_input("Empresa de Envío")
        numero_guia = st.text_input("Número de Guía")
        fecha_entrega_estimada = st.date_input("Fecha de Entrega Estimada")
        estado_envio = st.selectbox("Estado de Envío", ["pendiente", "en tránsito", "entregado", "fallido"])
        direccion_entrega = st.text_area("Dirección de Entrega")
        observaciones = st.text_area("Observaciones")
        submitted = st.form_submit_button("Agregar Envío")
        if submitted:
            insert_envio(conn, id_pedido, empresa_envio, numero_guia, str(fecha_entrega_estimada), estado_envio, direccion_entrega, observaciones)
            st.success("Envío agregado exitosamente")

with tab_reseñas:
    st.header("Agregar Reseña")
    with st.form("reseña_form"):
        id_usuario = st.number_input("ID Usuario", min_value=1, step=1)
        id_producto = st.number_input("ID Producto", min_value=1, step=1)
        calificacion = st.slider("Calificación", 1, 5)
        comentario = st.text_area("Comentario")
        submitted = st.form_submit_button("Agregar Reseña")
        if submitted:
            insert_reseña(conn, id_usuario, id_producto, calificacion, comentario)
            st.success("Reseña agregada exitosamente")

with tab_inventario:
    st.header("Agregar Movimiento de Inventario")
    with st.form("inventario_form"):
        id_producto = st.number_input("ID Producto", min_value=1, step=1)
        tipo_movimiento = st.selectbox("Tipo de Movimiento", ["entrada", "salida", "ajuste", "devolución"])
        cantidad = st.number_input("Cantidad", step=1)
        motivo = st.text_area("Motivo")
        usuario_responsable = st.number_input("Usuario Responsable", min_value=1, step=1)
        submitted = st.form_submit_button("Agregar Movimiento de Inventario")
        if submitted:
            insert_inventario(conn, id_producto, tipo_movimiento, cantidad, motivo, usuario_responsable)
            st.success("Movimiento de inventario agregado exitosamente")

with tab_historial:
    st.header("Agregar Historial de Acceso")
    with st.form("historial_form"):
        id_usuario = st.number_input("ID Usuario", min_value=1, step=1)
        accion_realizada = st.text_input("Acción Realizada")
        ip_usuario = st.text_input("IP Usuario")
        navegador = st.text_input("Navegador")
        submitted = st.form_submit_button("Agregar Historial de Acceso")
        if submitted:
            insert_historial_acceso(conn, id_usuario, accion_realizada, ip_usuario, navegador)
            st.success("Historial de acceso agregado exitosamente")

conn.close()
