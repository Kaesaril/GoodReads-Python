# 📚 GoodsReads

**GoodsReads** es una aplicación web desarrollada en Python con Flask que permite a los usuarios puntuar libros, dejar comentarios, y votar opiniones ajenas, todo ello en una interfaz intuitiva, ligera y modular. El almacenamiento de datos se realiza mediante objetos persistidos usando Sirope sobre Redis.

---

## 🚀 Funcionalidades Principales

- 📖 Visualizar un listado de libros
- ➕ Añadir, editar y eliminar libros
- ⭐ Puntuar libros
- 💬 Comentar libros y ver comentarios
- 👍👎 Votar comentarios de otros usuarios
- 👤 Autenticación de usuarios con sistema de login/registro

---

## 🧰 Tecnologías Utilizadas

| Capa        | Tecnología                  |
|-------------|-----------------------------|
| Backend     | Python 3.8+, Flask          |
| Frontend    | HTML5, Jinja2, Bootstrap    |
| Almacenamiento | Sirope + Redis             |
| Modularidad | Flask Blueprints            |

---

## 🗃️ Estructura del Proyecto

GoodsReads/
├── src/
│ ├── auth/ # Rutas de autenticación
│ ├── books/ # Lógica de libros
│ ├── comments/ # Comentarios y votos
│ ├── models/ # Clases persistidas
│ ├── templates/ # Vistas HTML
│ └── app.py # Entrada principal
├── doc/
│ └── memoria.pdf
├── README.md

yaml
Copiar
Editar

---

## 🛠️ Instalación

```bash
git clone https://github.com/tuusuario/goodsreads.git
cd goodsreads
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd src
(O abrir en el terminal redis-server)
python app.py
Accede a: http://127.0.0.1:5000/

