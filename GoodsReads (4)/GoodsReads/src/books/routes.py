from flask import render_template, redirect, url_for, request
from flask_login import login_required, current_user
import sirope

from src.models.libro import Libro
from src.models.usuario import Usuario
from src.models.puntuacion import Puntuacion
from src.models.comentario import Comentario
from src.models.VotoComentario import VotoComentario

from . import books_bp

srp = sirope.Sirope()

@books_bp.route("/")
@login_required
def home():
    libros = list(srp.load_all(Libro))
    libros = [libro for libro in libros if not getattr(libro, "borrado", False)]

    q = request.args.get("q")
    if q:
        libros = [libro for libro in libros if q.lower() in libro.titulo.lower() or q.lower() in libro.autor.lower()]

    return render_template("home.html", user=current_user, libros=libros, current_user=current_user, q=q)

@books_bp.route("/add_book", methods=["GET", "POST"])
@login_required
def add_book():
    if request.method == "POST":
        titulo = request.form["titulo"]
        autor = request.form["autor"]
        libro = Libro(titulo, autor, current_user.email)
        srp.save(libro)
        return redirect(url_for("books.home"))

    return render_template("add_book.html")

@books_bp.route("/book/<libro_titulo>")
@login_required
def view_book(libro_titulo):
    libro = next((l for l in srp.load_all(Libro) if l.titulo == libro_titulo and not getattr(l, "borrado", False)), None)

    if not libro:
        return redirect(url_for("books.home"))

    comentarios = [c for c in srp.load_all(Comentario)
                   if c.libro_titulo == libro_titulo and not getattr(c, "borrado", False)]

    puntuaciones = [p for p in srp.load_all(Puntuacion) if p.libro_titulo == libro_titulo]

    votos = {}
    for v in srp.load_all(VotoComentario):
        if v.comentario_id not in votos:
            votos[v.comentario_id] = 0
        votos[v.comentario_id] += v.valor

    return render_template("view_book.html", libro=libro, comentarios=comentarios,
                           puntuaciones=puntuaciones, votos=votos)

@books_bp.route("/edit_book/<libro_titulo>", methods=["GET", "POST"])
@login_required
def edit_book(libro_titulo):
    libro = next((l for l in srp.load_all(Libro) if l.titulo == libro_titulo and not getattr(l, "borrado", False)), None)

    if not libro:
        return redirect(url_for("books.home"))

    if not (current_user.is_admin() or libro.usuario_email == current_user.email):
        return redirect(url_for("books.home"))

    if request.method == "POST":
        libro.titulo = request.form["titulo"]
        libro.autor = request.form["autor"]
        srp.save(libro)
        return redirect(url_for("books.home"))

    return render_template("edit_book.html", libro=libro)

@books_bp.route("/delete_book/<libro_titulo>", methods=["POST"])
@login_required
def delete_book(libro_titulo):
    srp = sirope.Sirope()

    libro = next((l for l in srp.load_all(Libro) if l.titulo == libro_titulo and not getattr(l, "borrado", False)), None)

    if libro and (current_user.is_admin() or libro.usuario_email == current_user.email):
        libro.borrado = True
        srp.save(libro)

        # Borrar también los comentarios asociados
        for comentario in srp.load_all(Comentario):
            if comentario.libro_titulo == libro_titulo and not getattr(comentario, "borrado", False):
                comentario.borrado = True
                srp.save(comentario)

    return redirect(url_for("books.home"))


@books_bp.route("/rate_book/<libro_titulo>", methods=["POST"])
@login_required
def rate_book(libro_titulo):
    valor = int(request.form["valor"])

    if valor < 1 or valor > 5:
        return redirect(url_for("books.view_book", libro_titulo=libro_titulo))

    for puntuacion in srp.load_all(Puntuacion):
        if puntuacion.libro_titulo == libro_titulo and puntuacion.usuario_email == current_user.email:
            puntuacion.valor = valor
            srp.save(puntuacion)
            break
    else:
        nueva_puntuacion = Puntuacion(libro_titulo, current_user.email, valor)
        srp.save(nueva_puntuacion)

    return redirect(url_for("books.view_book", libro_titulo=libro_titulo))

@books_bp.route("/profile/<usuario_email>")
@login_required
def profile(usuario_email):
    usuario = next((u for u in srp.load_all(Usuario) if u.email == usuario_email), None)

    if not usuario:
        return redirect(url_for("books.home"))

    libros = [libro for libro in srp.load_all(Libro) if libro.usuario_email == usuario_email and not getattr(libro, "borrado", False)]
    comentarios = [comentario for comentario in srp.load_all(Comentario) if comentario.usuario_email == usuario_email and not getattr(comentario, "borrado", False)]

    puntuaciones = []
    for libro in libros:
        puntuaciones += [p for p in srp.load_all(Puntuacion) if p.libro_titulo == libro.titulo]

    media_puntuacion = sum(p.valor for p in puntuaciones) / len(puntuaciones) if puntuaciones else None

    return render_template("profile.html", usuario=usuario, libros=libros, comentarios=comentarios, media_puntuacion=media_puntuacion)
