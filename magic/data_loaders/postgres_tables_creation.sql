CREATE TABLE IF NOT EXISTS ventas (
    id SERIAL PRIMARY KEY,
    producto VARCHAR(255),
    cantidad INT,
    precio_unitario DECIMAL(10, 2),
    fecha_venta DATE
);
