import sqlite3
from random import choice

# Conexión a la base de datos SQLite
conn = sqlite3.connect("tps.db")
cursor = conn.cursor()

# Crear tablas si no existen
cursor.execute("""
CREATE TABLE IF NOT EXISTS clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS productos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    precio REAL NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS transacciones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id INTEGER,
    producto_id INTEGER,
    fecha TEXT NOT NULL,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id),
    FOREIGN KEY (producto_id) REFERENCES productos(id)
)
""")
conn.commit()

# Función para registrar un cliente
def registrar_cliente(nombre, email):
    try:
        cursor.execute("INSERT INTO clientes (nombre, email) VALUES (?, ?)", (nombre, email))
        conn.commit()
        print(f"Cliente {nombre} registrado con éxito.")
    except sqlite3.IntegrityError:
        print("⚠️ Error: El correo ya está registrado.")

# Función para añadir productos
def añadir_producto(nombre, precio):
    cursor.execute("INSERT INTO productos (nombre, precio) VALUES (?, ?)", (nombre, precio))
    conn.commit()
    print(f"Producto {nombre} agregado con precio {precio}€.")

# Función para realizar una compra
def realizar_compra(email, producto_id):
    cursor.execute("SELECT id FROM clientes WHERE email = ?", (email,))
    cliente = cursor.fetchone()
    
    if cliente:
        cursor.execute("INSERT INTO transacciones (cliente_id, producto_id, fecha) VALUES (?, ?, datetime('now'))",
                       (cliente[0], producto_id))
        conn.commit()
        print("✅ Compra realizada con éxito.")
    else:
        print("⚠️ Error: Cliente no encontrado.")

# Función para mostrar historial de transacciones
def mostrar_transacciones():
    cursor.execute("""
    SELECT t.id, c.nombre, p.nombre, p.precio, t.fecha 
    FROM transacciones t 
    JOIN clientes c ON t.cliente_id = c.id
    JOIN productos p ON t.producto_id = p.id
    """)
    transacciones = cursor.fetchall()
    
    print("\n📜 Historial de Transacciones:")
    for transaccion in transacciones:
        print(f"ID {transaccion[0]} - Cliente: {transaccion[1]} - Producto: {transaccion[2]} - Precio: {transaccion[3]}€ - Fecha: {transaccion[4]}")

# Funciones para generar informes de gestión (KPIs)        

def mostrar_informes_financieros(fecha_inicio, fecha_fin):
    cursor.execute("""
        SELECT SUM(p.precio) AS total_ventas, COUNT(*) AS num_transacciones, 
               (SUM(p.precio)*1.0 / COUNT(*)) AS ticket_medio
        FROM transacciones t
        JOIN productos p ON t.producto_id = p.id
        WHERE t.fecha BETWEEN ? AND ?
    """, (fecha_inicio, fecha_fin))
    resultado = cursor.fetchone()
    
    if resultado and resultado[1] > 0:
        total, num, ticket = resultado
        print(f"\nInforme Financiero ({fecha_inicio} a {fecha_fin}):")
        print(f"  Total de Ventas: {total:.2f}€")
        print(f"  Número de Transacciones: {num}")
        print(f"  Ticket Promedio: {ticket:.2f}€")
    else:
        print("No hay datos para el período seleccionado.")

def mostrar_producto_mas_vendido(fecha_inicio, fecha_fin):
    cursor.execute("""
        SELECT p.nombre, COUNT(*) AS cantidad_vendida
        FROM transacciones t
        JOIN productos p ON t.producto_id = p.id
        WHERE t.fecha BETWEEN ? AND ?
        GROUP BY p.nombre
        ORDER BY cantidad_vendida DESC
        LIMIT 1
    """, (fecha_inicio, fecha_fin))
    resultado = cursor.fetchone()
    
    if resultado:
        nombre_producto, cantidad = resultado
        print(f"\nProducto Más Vendido ({fecha_inicio} a {fecha_fin}): {nombre_producto} con {cantidad} ventas")
    else:
        print("No se encontraron ventas en el período seleccionado.")

def mostrar_informes_gestion():
    fecha_inicio = input("Introduce la fecha de inicio (YYYY-MM-DD): ")
    fecha_fin = input("Introduce la fecha de fin (YYYY-MM-DD): ")
    
    # Mostrar el informe financiero y el producto más vendido para el rango ingresado.
    mostrar_informes_financieros(fecha_inicio, fecha_fin)
    mostrar_producto_mas_vendido(fecha_inicio, fecha_fin)

def insertar_registros_ejemplo():
    # Datos de ejemplo para clientes
    clientes_ejemplo = [
        ("Ana", "ana@example.com"),
        ("Luis", "luis@example.com"),
        ("Marta", "marta@example.com"),
        ("Carlos", "carlos@example.com"),
        ("Elena", "elena@example.com")
    ]
    
    # Inserción de clientes
    for nombre, email in clientes_ejemplo:
        registrar_cliente(nombre, email)
    
    # Datos de ejemplo para productos
    productos_ejemplo = [
        ("Televisor 40\"", 399.99),
        ("Laptop", 899.99),
        ("Smartphone", 499.99),
        ("Cámara Digital", 299.99),
        ("Auriculares", 59.99)
    ]
    
    
    for nombre, precio in productos_ejemplo:
        añadir_producto(nombre, precio)
    
    
    emails = [email for _, email in clientes_ejemplo]
    num_productos = len(productos_ejemplo)
    
    for i in range(10):
        email = choice(emails)
        producto_id = choice(range(1, num_productos + 1))
        realizar_compra(email, producto_id)


insertar_registros_ejemplo()



# Menú en consola para probar el sistema
def menu():
    while True:
        print("\n=== Sistema de Procesamiento de Transacciones (TPS) ===")
        print("1️⃣ Registrar Cliente")
        print("2️⃣ Añadir Producto")
        print("3️⃣ Realizar Compra")
        print("4️⃣ Ver Historial de Transacciones")
        print("5️⃣ Ver Informes de Gestión")
        print("6️⃣ Salir")

        
        opcion = input("Selecciona una opción: ")
        
        if opcion == "1":
            nombre = input("Nombre del cliente: ")
            email = input("Email del cliente: ")
            registrar_cliente(nombre, email)
        elif opcion == "2":
            nombre = input("Nombre del producto: ")
            precio = float(input("Precio del producto: "))
            añadir_producto(nombre, precio)
        elif opcion == "3":
            email = input("Email del cliente: ")
            producto_id = int(input("ID del producto: "))
            realizar_compra(email, producto_id)
        elif opcion == "4":
            mostrar_transacciones()
        elif opcion == "5":
            mostrar_informes_gestion()
        elif opcion == "6":
            print("👋 Saliendo del sistema...")
            conn.close()
            break
        else:
            print("⚠️ Opción no válida, intenta de nuevo.")

# Ejecutar menú
menu()