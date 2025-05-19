import sqlite3

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

# Menú en consola para probar el sistema
def menu():
    while True:
        print("\n=== Sistema de Procesamiento de Transacciones (TPS) ===")
        print("1️⃣ Registrar Cliente")
        print("2️⃣ Añadir Producto")
        print("3️⃣ Realizar Compra")
        print("4️⃣ Ver Historial de Transacciones")
        print("5️⃣ Salir")
        
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
            print("👋 Saliendo del sistema...")
            conn.close()
            break
        else:
            print("⚠️ Opción no válida, intenta de nuevo.")

# Ejecutar menú
menu()