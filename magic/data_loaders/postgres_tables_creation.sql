CREATE TABLE IF NOT EXISTS ventas (
    id SERIAL PRIMARY KEY,
    producto VARCHAR(255),
    cantidad INT,
    precio_unitario DECIMAL(10, 2),
    fecha_venta DATE
);

CREATE TABLE IF NOT EXISTS detalle_ventas (
    id SERIAL PRIMARY KEY,
    producto VARCHAR(100) NOT NULL,
    cantidad INT NOT NULL,
    precio_unitario DECIMAL(10,2) NOT NULL,
    fecha_venta TIMESTAMP NOT NULL,
    total_venta DECIMAL(10,2),
    categoria_venta VARCHAR(10),
    mes_venta INT
);
