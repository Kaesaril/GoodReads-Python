from flask import request, redirect, url_for
from flask_login import login_required, current_user
import sirope

from src.models.comentario import Comentario
from src.models.VotoComentario import VotoComentario

from . import comments_bp

srp = sirope.Sirope()

@comments_bp.route("/add_comment/<libro_titulo>", methods=["POST"])
@login_required
def add_comment(libro_titulo):
    texto = request.form["texto"].strip()
    if not texto:
        return redirect(url_for("books.view_book", libro_titulo=libro_titulo))

    comentario = Comentario(libro_titulo, current_user.email, texto)
    srp.save(comentario)
    return redirect(url_for("books.view_book", libro_titulo=libro_titulo))

@comments_bp.route("/reply_comment/<libro_titulo>/<parent_texto>", methods=["POST"])
@login_required
def reply_comment(libro_titulo, parent_texto):
    texto = request.form["texto"].strip()
    if not texto:
        return redirect(url_for("books.view_book", libro_titulo=libro_titulo))

    comentario = Comentario(libro_titulo, current_user.email, texto, comentario_padre=parent_texto)
    srp.save(comentario)
    return redirect(url_for("books.view_book", libro_titulo=libro_titulo))

@comments_bp.route("/delete_comment/<libro_titulo>/<comentario_id>", methods=["POST"])
@login_required
def delete_comment(libro_titulo, comentario_id):
    for comentario in srp.load_all(Comentario):
        if comentario.id == comentario_id and not getattr(comentario, "borrado", False):
            if current_user.is_admin() or comentario.usuario_email == current_user.email:
                comentario.borrado = True
                srp.save(comentario)
            break

    return redirect(url_for("books.view_book", libro_titulo=libro_titulo))

@comments_bp.route("/vote_comment/<libro_titulo>/<comentario_id>", methods=["POST"])
@login_required
def vote_comment(libro_titulo, comentario_id):
    valor = int(request.form["valor"])

    for voto in srp.load_all(VotoComentario):
        if voto.comentario_id == comentario_id and voto.usuario_email == current_user.email:
            voto.valor = valor
            srp.save(voto)
            break
    else:
        nuevo_voto = VotoComentario(comentario_id, current_user.email, valor)
        srp.save(nuevo_voto)

    return redirect(url_for("books.view_book", libro_titulo=libro_titulo))
