from flask import Flask, render_template, request, redirect, session, url_for, flash
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Inicializar la sesión con una lista vacía de productos
@app.before_request
def iniciar_sesion():
    if 'productos' not in session:
        session['productos'] = []

# Página de inicio que lista los productos
@app.route('/')
def home():
    return render_template('home.html', productos=session['productos'])

# Ruta para agregar un nuevo producto
@app.route('/agregar', methods=['GET', 'POST'])
def agregar_producto():
    if request.method == 'POST':
        nuevo_producto = {
            'id': request.form['id'],
            'nombre': request.form['nombre'],
            'cantidad': int(request.form['cantidad']),
            'precio': float(request.form['precio']),
            'fecha_vencimiento': request.form['fecha_vencimiento'],
            'categoria': request.form['categoria']
        }

        # Verificar que el ID sea único
        for producto in session['productos']:
            if producto['id'] == nuevo_producto['id']:
                flash('El ID del producto debe ser único.', 'error')
                return redirect(url_for('agregar_producto'))

        session['productos'].append(nuevo_producto)
        session.modified = True  # Indicar que la sesión ha sido modificada
        flash('Producto agregado con éxito.', 'success')
        return redirect(url_for('home'))
    
    return render_template('add_product.html')

# Ruta para editar un producto existente
@app.route('/editar/<id>', methods=['GET', 'POST'])
def editar_producto(id):
    producto = next((p for p in session['productos'] if p['id'] == id), None)
    if not producto:
        flash('Producto no encontrado.', 'error')
        return redirect(url_for('home'))

    if request.method == 'POST':
        producto['nombre'] = request.form['nombre']
        producto['cantidad'] = int(request.form['cantidad'])
        producto['precio'] = float(request.form['precio'])
        producto['fecha_vencimiento'] = request.form['fecha_vencimiento']
        producto['categoria'] = request.form['categoria']
        session.modified = True
        flash('Producto editado con éxito.', 'success')
        return redirect(url_for('home'))
    
    return render_template('edit_product.html', producto=producto)

# Ruta para eliminar un producto
@app.route('/eliminar/<id>', methods=['POST'])
def eliminar_producto(id):
    session['productos'] = [p for p in session['productos'] if p['id'] != id]
    session.modified = True
    flash('Producto eliminado con éxito.', 'success')
    return redirect(url_for('home'))

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run(debug=True)
