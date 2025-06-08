from flask import Flask
from flask_login import LoginManager
import sirope

# Importar modelos y blueprints
from src.models.usuario import Usuario
from src.auth import auth_bp
from src.books import books_bp
from src.comments import comments_bp

# Crear la app Flask
app = Flask(__name__)
app.secret_key = "clave_secreta"

# Inicializar sirope y login manager
srp = sirope.Sirope()
login_manager = LoginManager(app)
login_manager.login_view = "auth.login"

# Cargar usuario
@login_manager.user_loader
def load_user(email):
    return next(srp.filter(Usuario, lambda u: u.email == email), None)

# Registrar Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(books_bp)
app.register_blueprint(comments_bp)

# Iniciar servidor
if __name__ == "__main__":
    app.run(debug=True)
