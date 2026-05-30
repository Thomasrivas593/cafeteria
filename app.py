from flask import Flask, render_template, request, redirect
import sqlite3
from modelo import inicializar_db, Producto

app = Flask(__name__)

# Ejecutamos la función para asegurar que la tabla exista al iniciar
inicializar_db() 

@app.route('/')
def index():
    # 1. Nos conectamos y pedimos todos los productos
    conexion = sqlite3.connect('cafeteria.db')
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM productos")
    productos_db = cursor.fetchall()
    conexion.close()
    # 2. Calculamos el valor total llamando a nuestro nuevo método
    total_invertido = Producto.calcular_valor_inventario()
    
    # 2. Le pasamos esos datos al archivo HTML para que arme la tabla
    return render_template('index.html', productos=productos_db, valor_total=total_invertido )

@app.route('/vender/<int:id>', methods=['POST'])
def vender(id):
    # Aquí iría la lógica para restar stock en la base de datos
    # 1. Buscamos el producto en la base de datos y lo convertimos en un objeto
    producto_a_vender = Producto.obtener_por_id(id)
    
    # 2. Si el producto existe, usamos su método para vender 1 unidad
    if producto_a_vender:
        producto_a_vender.vender(1)
        
    # 3. Recargamos la página para ver el stock actualizado
    return redirect('/')
    
    

@app.route('/agregar', methods=['POST'])
def agregar():
    # 1. Atrapamos los datos que el usuario escribió en el formulario web
    nombre = request.form['nombre']
    categoria = request.form['categoria']
    precio = float(request.form['precio'])
    stock = int(request.form['stock'])
    
    # 2. Aplicamos la Programación Orientada a Objetos: 
    # Usamos la clase (el molde) para crear un nuevo objeto producto (la instancia)
    nuevo_producto = Producto(nombre, categoria, precio, stock)
    
    # 3. Guardamos el objeto en la base de datos
    nuevo_producto.guardar_en_db()
    
    # 4. Redirigimos a la página principal para ver la tabla actualizada
    return redirect('/')
@app.route('/reponer/<int:id>', methods=['POST'])
def reponer_stock(id):
    # Atrapamos la cantidad exacta que el usuario escribió en la tabla
    cantidad = int(request.form['cantidad_reposicion'])
    
    # Buscamos el objeto y usamos su nuevo método
    producto_a_reponer = Producto.obtener_por_id(id)
    if producto_a_reponer:
        producto_a_reponer.reponer(cantidad)
        
    return redirect('/')
if __name__ == '__main__':
    app.run(debug=True)