from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Veritabanı nesnesini burada tanımlıyoruz
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Flask yapılandırma ayarları
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # SQLite kullanıyoruz
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # SQLAlchemy'nin otomatik takip etmesini kapatalım

    # Yükleme ile ilgili ayarlar
    app.config['UPLOAD_FOLDER'] = 'app/static/uploads'
    app.config['ALLOWED_EXTENSIONS'] = {'mp4', 'mov', 'avi'}
    app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # Maksimum dosya boyutu (50MB)

    # db'yi uygulamaya bağlayalım
    db.init_app(app)

    # Blueprint'leri burada kaydediyoruz
    from .routes import main  # routes.py dosyasını burada import ediyoruz
    app.register_blueprint(main)

    return app