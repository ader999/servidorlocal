from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
db = SQLAlchemy(app)



class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    categoria = db.Column(db.String(50), nullable=False)
    imagen = db.Column(db.String(200))

class Configuracion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre_negocio=db.Column(db.String(100),nullable=False)
    direccion = db.Column(db.String(200))
    email_contacto = db.Column(db.String(120))
    telefono_contacto = db.Column(db.String(20))
    horario_apertura = db.Column(db.String(20))
    horario_cierre = db.Column(db.String(20))
    sitio_web = db.Column(db.String(100))
    redes_sociales = db.Column(db.String(200))
    categoria=db.Column(db.String(50),nullable=False)
    
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    primerysegundo_nombre =db.Column(db.String(80), nullable=False)
    primerysegundo_apellido =db.Column(db.String(80), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    categoria = db.Column(db.String(50), unique=True, nullable=False)


@app.route('/')
def index():
    # Verificar si ya se han configurado los datos
    if Configuracion.query.count() == 0:
        return redirect('/configuracion')
        
    productos = Producto.query.all()
    return render_template('index.html', productos=productos)

@app.route('/panel_control')
def panel_control():
    # Aquí puedes agregar lógica para mostrar datos y funcionalidades del panel de control
    return render_template('panel_control.html')


@app.route('/configuracion', methods=['GET', 'POST'])
def configuracion():
    if request.method == 'POST':
        # Procesar el formulario y guardar los datos
        nombre_negocio = request.form['nombre_negocio']
        categoria = request.form['categoria']
        config = Configuracion(nombre_negocio=nombre_negocio, categoria=categoria)
        db.session.add(config)
        db.session.commit()
        return redirect('/')
    
    return render_template('configuracion.html')



@app.route('/agregar', methods=['POST', 'GET'])
def agregar_producto():
    if request.method == 'POST':
        nombre = request.form['nombre']
        precio = request.form['precio']
        categoria = request.form['categoria']
        imagen = request.form['imagen']
        producto = Producto(nombre=nombre, precio=precio, categoria=categoria, imagen=imagen)
        db.session.add(producto)
        db.session.commit()
        return redirect('/')
    return render_template('agregar_producto.html')

@app.route('/editar/<int:id>', methods=['POST', 'GET'])
def editar_producto(id):
    producto = Producto.query.get(id)
    if request.method == 'POST':
        producto.nombre = request.form['nombre']
        producto.precio = request.form['precio']
        producto.categoria = request.form['categoria']
        producto.imagen = request.form['imagen']
        db.session.commit()
        return redirect('/')
    return render_template('editar_producto.html', producto=producto)

@app.route('/eliminar/<int:id>')
def eliminar_producto(id):
    producto = Producto.query.get(id)
    db.session.delete(producto)
    db.session.commit()
    return redirect('/')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000,debug=True)
