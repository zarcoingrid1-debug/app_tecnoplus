
-- 1. Usuarios
CREATE TABLE IF NOT EXISTS Usuarios (
    id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    correo_electronico TEXT UNIQUE NOT NULL,
    contraseña TEXT NOT NULL,
    telefono TEXT,
    direccion TEXT,
    rol INTEGER,
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
    estado BOOLEAN DEFAULT 1
);

-- 2. Productos
CREATE TABLE IF NOT EXISTS Productos (
    id_producto INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    descripcion TEXT,
    id_categoria INTEGER,
    id_marca INTEGER,
    precio DECIMAL(10,2) NOT NULL,
    stock INTEGER DEFAULT 0,
    imagen_url TEXT,
    estado BOOLEAN DEFAULT 1,
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_categoria) REFERENCES Categorias(id_categoria),
    FOREIGN KEY (id_marca) REFERENCES Marcas(id_marca)
);

-- 3. Categorias
CREATE TABLE IF NOT EXISTS Categorias (
    id_categoria INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    descripcion TEXT,
    estado BOOLEAN DEFAULT 1,
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 4. Pedidos
CREATE TABLE IF NOT EXISTS Pedidos (
    id_pedido INTEGER PRIMARY KEY AUTOINCREMENT,
    id_usuario INTEGER NOT NULL,
    fecha_pedido DATETIME DEFAULT CURRENT_TIMESTAMP,
    total DECIMAL(10,2) NOT NULL,
    estado TEXT CHECK(estado IN ('pendiente','pagado','enviado','cancelado')) DEFAULT 'pendiente',
    observaciones TEXT,
    direccion_envio TEXT,
    FOREIGN KEY (id_usuario) REFERENCES Usuarios(id_usuario)
);

-- 5. Detalle_Pedido
CREATE TABLE IF NOT EXISTS Detalle_Pedido (
    id_detalle INTEGER PRIMARY KEY AUTOINCREMENT,
    id_pedido INTEGER NOT NULL,
    id_producto INTEGER NOT NULL,
    cantidad INTEGER NOT NULL,
    precio_unitario DECIMAL(10,2) NOT NULL,
    subtotal DECIMAL(10,2) GENERATED ALWAYS AS (cantidad * precio_unitario) STORED,
    FOREIGN KEY (id_pedido) REFERENCES Pedidos(id_pedido),
    FOREIGN KEY (id_producto) REFERENCES Productos(id_producto)
);

-- 6. Carrito
CREATE TABLE IF NOT EXISTS Carrito (
    id_carrito INTEGER PRIMARY KEY AUTOINCREMENT,
    id_usuario INTEGER NOT NULL,
    id_producto INTEGER NOT NULL,
    cantidad INTEGER NOT NULL,
    fecha_agregado DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_usuario) REFERENCES Usuarios(id_usuario),
    FOREIGN KEY (id_producto) REFERENCES Productos(id_producto)
);

-- 7. Pagos
CREATE TABLE IF NOT EXISTS Pagos (
    id_pago INTEGER PRIMARY KEY AUTOINCREMENT,
    id_pedido INTEGER NOT NULL,
    monto_pagado DECIMAL(10,2) NOT NULL,
    metodo_pago TEXT CHECK(metodo_pago IN ('tarjeta','transferencia','efectivo','paypal')),
    estado_pago TEXT CHECK(estado_pago IN ('pendiente','aprobado','rechazado')) DEFAULT 'pendiente',
    fecha_pago DATETIME DEFAULT CURRENT_TIMESTAMP,
    referencia_transaccion TEXT,
    FOREIGN KEY (id_pedido) REFERENCES Pedidos(id_pedido)
);

-- 8. Envios
CREATE TABLE IF NOT EXISTS Envios (
    id_envio INTEGER PRIMARY KEY AUTOINCREMENT,
    id_pedido INTEGER NOT NULL,
    empresa_envio TEXT,
    numero_guia TEXT,
    fecha_envio DATETIME DEFAULT CURRENT_TIMESTAMP,
    fecha_entrega_estimada DATETIME,
    estado_envio TEXT CHECK(estado_envio IN ('pendiente','en tránsito','entregado','fallido')) DEFAULT 'pendiente',
    direccion_entrega TEXT,
    observaciones TEXT,
    FOREIGN KEY (id_pedido) REFERENCES Pedidos(id_pedido)
);

-- 9. Reseñas
CREATE TABLE IF NOT EXISTS Reseñas (
    id_reseña INTEGER PRIMARY KEY AUTOINCREMENT,
    id_usuario INTEGER NOT NULL,
    id_producto INTEGER NOT NULL,
    calificacion INTEGER CHECK(calificacion BETWEEN 1 AND 5),
    comentario TEXT,
    fecha_reseña DATETIME DEFAULT CURRENT_TIMESTAMP,
    estado BOOLEAN DEFAULT 1,
    FOREIGN KEY (id_usuario) REFERENCES Usuarios(id_usuario),
    FOREIGN KEY (id_producto) REFERENCES Productos(id_producto)
);

-- 10. Inventario
CREATE TABLE IF NOT EXISTS Inventario (
    id_movimiento INTEGER PRIMARY KEY AUTOINCREMENT,
    id_producto INTEGER NOT NULL,
    tipo_movimiento TEXT CHECK(tipo_movimiento IN ('entrada','salida','ajuste','devolución')),
    cantidad INTEGER NOT NULL,
    fecha_movimiento DATETIME DEFAULT CURRENT_TIMESTAMP,
    motivo TEXT,
    usuario_responsable INTEGER,
    FOREIGN KEY (id_producto) REFERENCES Productos(id_producto),
    FOREIGN KEY (usuario_responsable) REFERENCES Usuarios(id_usuario)
);

-- 11. Historial_Acceso
CREATE TABLE IF NOT EXISTS Historial_Acceso (
    id_acceso INTEGER PRIMARY KEY AUTOINCREMENT,
    id_usuario INTEGER NOT NULL,
    fecha_hora DATETIME DEFAULT CURRENT_TIMESTAMP,
    accion_realizada TEXT,
    ip_usuario TEXT,
    navegador TEXT,
    FOREIGN KEY (id_usuario) REFERENCES Usuarios(id_usuario)
);
