from datetime import datetime

class Libro:
    def __init__(self, titulo, autor, usuario_email):
        self.titulo = titulo
        self.autor = autor
        self.usuario_email = usuario_email
        self.borrado = False
        self.fecha = datetime.now()  # Añadimos la fecha al crearse
