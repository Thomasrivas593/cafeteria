import sqlite3

def inicializar_db():
    # Se conecta al archivo (si no existe, lo crea)
    conexion = sqlite3.connect('cafeteria.db')
    cursor = conexion.cursor()
    # Crea la tabla con la estructura solicitada en la consigna
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            categoria TEXT NOT NULL,
            precio REAL NOT NULL,
            stock INTEGER NOT NULL,
            disponible BOOLEAN NOT NULL
        )
    ''')
    conexion.commit()
    conexion.close()

class Producto:
    def __init__(self, nombre, categoria, precio, stock, disponible=True, id=None):
        self.id = id
        self.nombre = nombre
        self.categoria = categoria
        self.precio = precio
        self.stock = stock
        self.disponible = disponible

    def guardar_en_db(self):
        # Este método inserta el objeto instanciado en la base de datos
        conexion = sqlite3.connect('cafeteria.db')
        cursor = conexion.cursor()
        cursor.execute('''
            INSERT INTO productos (nombre, categoria, precio, stock, disponible)
            VALUES (?, ?, ?, ?, ?)
        ''', (self.nombre, self.categoria, self.precio, self.stock, self.disponible))
        conexion.commit()
        conexion.close()
    @staticmethod
    def obtener_por_id(id_producto):
        # Busca un producto específico en la BD y crea el objeto
        conexion = sqlite3.connect('cafeteria.db')
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM productos WHERE id = ?", (id_producto,))
        fila = cursor.fetchone()
        conexion.close()
        
        if fila:
            # Crea y retorna la instancia usando los datos de la BD
            return Producto(id=fila[0], nombre=fila[1], categoria=fila[2], 
                            precio=fila[3], stock=fila[4], disponible=fila[5])
        return None

    def vender(self, cantidad):
        # Lógica de negocio usando 'self'
        if self.stock >= cantidad:
            self.stock -= cantidad
            if self.stock == 0:
                self.disponible = False
            
            # Guardamos el cambio de este objeto en la base de datos
            conexion = sqlite3.connect('cafeteria.db')
            cursor = conexion.cursor()
            cursor.execute('''
                UPDATE productos 
                SET stock = ?, disponible = ?
                WHERE id = ?
            ''', (self.stock, self.disponible, self.id))
            conexion.commit()
            conexion.close()    
    def reponer(self, cantidad):
        # 1. Sumamos la cantidad al stock actual
        self.stock += cantidad
        
        # 2. Regla de negocio: si vuelve a tener stock, lo reactivamos
        if self.stock > 0:
            self.disponible = True
            
        # 3. Actualizamos la base de datos
        conexion = sqlite3.connect('cafeteria.db')
        cursor = conexion.cursor()
        cursor.execute('''
            UPDATE productos 
            SET stock = ?, disponible = ?
            WHERE id = ?
        ''', (self.stock, self.disponible, self.id))
        conexion.commit()
        conexion.close()      
    @staticmethod
    def calcular_valor_inventario():
        # Nos conectamos a la base de datos
        conexion = sqlite3.connect('cafeteria.db')
        cursor = conexion.cursor()
        
        # Le pedimos a SQLite que multiplique el precio por el stock y sume todo
        cursor.execute("SELECT SUM(precio * stock) FROM productos")
        
        # Atrapamos el resultado (fetchone trae una tupla, sacamos el primer elemento [0])
        resultado = cursor.fetchone()[0]
        conexion.close()
        
        # Si la base de datos está vacía, devuelve 0. Si tiene datos, devuelve el total.
        return resultado if resultado else 0.0       