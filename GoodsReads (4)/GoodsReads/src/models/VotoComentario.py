class VotoComentario:
    def __init__(self, comentario_id, usuario_email, valor):
        self.comentario_id = comentario_id  # Será el id del comentario
        self.usuario_email = usuario_email  # Quién vota
        self.valor = valor  # +1 (like) o -1 (dislike)
