from flask import Flask, render_template, request, redirect, url_for, session
from pymongo import MongoClient
from datetime import datetime
import re

app = Flask(__name__)
app.secret_key = "seguridad2026"

# Conexión MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["banco_inseguro"]
coleccion = db["transacciones"]

# Usuarios del sistema
usuarios = {
    "admin": {
        "password": "admin123",
        "rol": "admin"
    },
    "operador": {
        "password": "operador123",
        "rol": "operador"
    }
}


@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        usuario = request.form['usuario']
        password = request.form['password']

        if usuario in usuarios and usuarios[usuario]["password"] == password:

            session["usuario"] = usuario
            session["rol"] = usuarios[usuario]["rol"]

            if session["rol"] == "admin":
                return redirect(url_for('admin'))

            return redirect(url_for('operador'))

        return "Usuario o contraseña incorrectos"

    return render_template("login.html")


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))



# OPERADOR

@app.route('/operador', methods=['GET', 'POST'])
def operador():

    if "rol" not in session:
        return redirect(url_for("login"))

    if session["rol"] != "operador":
        return "Acceso denegado"

    mensaje = ""

    if request.method == 'POST':

        nombre = request.form['nombre']
        apellido = request.form['apellido']

        if not re.match(r'^[A-Za-zÁÉÍÓÚáéíóúñÑ ]+$', nombre):
            return "Nombre inválido"

        if not re.match(r'^[A-Za-zÁÉÍÓÚáéíóúñÑ ]+$', apellido):
            return "Apellido inválido"

        datos = {
            "id": str(request.form['id']).strip(),
            "nombre": nombre,
            "apellido": apellido,
            "tipo": request.form['tipo'],
            "valor": request.form['valor'],
            "fecha_hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        coleccion.insert_one(datos)
        mensaje = "✅ Transacción guardada correctamente"

    return render_template('operador.html', mensaje=mensaje)



# ADMINISTRADOR

@app.route('/admin')
def admin():

    if "rol" not in session:
        return redirect(url_for("login"))

    if session["rol"] != "admin":
        return "Acceso denegado"

    id_buscar = str(request.args.get('id', '')).strip()

    if id_buscar and not re.match(r'^[A-Za-z0-9]+$', id_buscar):
        return "ID inválido"

    if id_buscar:
        registros = list(coleccion.find({"id": id_buscar}))
    else:
        registros = list(coleccion.find())

    return render_template(
        'admin.html',
        registros=registros,
        busqueda=id_buscar
    )


@app.route('/eliminar/<id_cliente>')
def eliminar(id_cliente):

    if "rol" not in session:
        return redirect(url_for("login"))

    if session["rol"] != "admin":
        return "Acceso denegado"

    coleccion.delete_one({"id": id_cliente})

    return redirect(url_for('admin'))


@app.route('/editar/<id_cliente>', methods=['GET', 'POST'])
def editar(id_cliente):

    if "rol" not in session:
        return redirect(url_for("login"))

    if session["rol"] != "admin":
        return "Acceso denegado"

    if request.method == 'POST':

        nuevos_datos = {
            "nombre": request.form['nombre'],
            "apellido": request.form['apellido'],
            "tipo": request.form['tipo'],
            "valor": request.form['valor']
        }

        coleccion.update_one(
            {"id": id_cliente},
            {"$set": nuevos_datos}
        )

        return redirect(url_for('admin'))

    registro = coleccion.find_one({"id": id_cliente})

    return render_template(
        'editar.html',
        registro=registro
    )


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)