# TPS - Sistema de Procesamiento de Transacciones
## Descripción
Este proyecto es un Sistema de Procesamiento de Transacciones (TPS) desarrollado en Python y basado en SQLite. Permite gestionar clientes, productos y transacciones de manera eficiente mediante una interfaz en consola
## Características
- Registro de clientes con validación de email.
- Gestión de productos con almacenamiento de precios.
- Registro de compras asociando clientes y productos.
- Historial de transacciones con detalles de cada operación.
- Base de datos persistente en SQLite, sin dependencias externas.
## Requisitos
- Python 3.x
- Módulo estándar sqlite3 (incluido en Python)
## Instalación y Ejecución
### Clonar el repositorio
```
git clone https://github.com/JorgeMV-MSMK/Strategic-Infromation-Systems-AB.git
cd Strategic-Information-Systems-AB
```
### Ejecutar el script
```
python Transaction_Processing_System.py
```
### Uso
- Registrar un cliente -> Ingresa su nombre y email
- Añadir un producto -> Define su nombre y precio
- Realizar una compra -> Selecciona un cliente y el producto adquirido
- Ver historial de transacciones -> Consulta todas las compras registradas

## Licencia
Este proyecto no está bajo ninguna licencia.

