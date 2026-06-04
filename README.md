# Proyecto programacion

#Descripción

Aplicación web desarrollada en Flask y MongoDB para la gestión de transacciones bancarias.

El proyecto implementa controles de seguridad para prevenir ataques XSS e Inyección NoSQL.

#Integrantes

* Dainner Salas
* Camilo Polo


# Tecnologías utilizadas

* Python 3
* Flask
* MongoDB
* Bootstrap
* Jinja2

#Medidas de seguridad implementadas

# Protección contra XSS

Se eliminaron los filtros `|safe` de las plantillas HTML para permitir el escape automático de caracteres especiales.

#Protección contra Inyección NoSQL

Se implementó validación mediante expresiones regulares para controlar los datos recibidos desde formularios y parámetros de búsqueda.

# Control de acceso por roles

Se implementó un sistema de autenticación con dos perfiles:

* Administrador
* Operador

Cada perfil tiene acceso únicamente a las funciones autorizadas.

# Instalación

# 1.  repositorio

https://github.com/Dainners/ProyectoSeguridad.git

### 2. Crear entorno virtual

python -m venv venv

# 3. Activar entorno virtual

Windows:

venv\Scripts\activate

#4. Instalar dependencias

pip install -r requirements.txt

#5. Iniciar MongoDB

Verificar que el servicio MongoDB esté ejecutándose.

# 6. Ejecutar aplicación

python app.py

# Usuarios de prueba

# Administrador

Usuario: admin

Contraseña: admin123

#Operador

Usuario: operador

Contraseña: operador123

#Estructura del proyecto

ProyectoSeguridad/

* app.py
* requirements.txt
* README.md
* templates/

  * login.html
  * admin.html
  * operador.html
  * editar.html
  * plantilla.html

#Evidencias

* Inicio de sesión por roles.
* Restricción de acceso según permisos.
* Protección XSS.
* Protección NoSQL Injection.
* Registro y consulta de transacciones.
