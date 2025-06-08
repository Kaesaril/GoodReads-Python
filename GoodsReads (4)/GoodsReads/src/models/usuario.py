from flask_login import UserMixin

class Usuario(UserMixin):
    def __init__(self, nombre, email, password, rol="usuario"):
        self.nombre = nombre
        self.email = email
        self.password = password
        self.rol = rol  # usuario o admin

    def get_id(self):
        return self.email

    def is_admin(self):
        # Si no tiene atributo rol, devolver False por defecto
        return getattr(self, "rol", "usuario") == "admin"
