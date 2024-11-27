import os
from flask import Blueprint, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

# Blueprint tanımlaması
main = Blueprint('main', __name__)

# Yükleme klasörü ve izin verilen dosya türleri
UPLOAD_FOLDER = 'app/static/uploads'
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Yüklenen videoları dosya sisteminden al
def get_uploaded_videos():
    videos = []
    # Video dosyalarını listeliyoruz
    for filename in os.listdir(UPLOAD_FOLDER):
        if allowed_file(filename):
            # Başlık olarak dosya adı alınabilir (başlık dosya adıyla ilişkili olabilir)
            video_title = filename.rsplit('.', 1)[0]  # Dosya adının uzantısını ayırıyoruz
            video_id = len(videos) + 1  # Her videoya benzersiz bir id veriyoruz
            videos.append({'id': video_id, 'title': video_title, 'filename': filename})
    return videos

# Ana sayfa rota
@main.route('/')
def home():
    videos = get_uploaded_videos()
    return render_template('home.html', videos=videos)

# Video yükleme sayfası
@main.route('/upload', methods=['GET', 'POST'])
def upload_video():
    if request.method == 'POST':
        title = request.form.get('title')  # Başlık alınır
        video_file = request.files.get('video')  # Video dosyası alınır
        
        if not title:
            return "Başlık gerekli", 400
        
        if video_file and allowed_file(video_file.filename):
            # Dosya adı güvenli hale getiriliyor
            video_filename = secure_filename(video_file.filename)
            
            # Başlıkla birlikte dosya adını kaydediyoruz
            title_filename = title + '.' + video_filename.rsplit('.', 1)[-1]
            
            # Dosya kaydediliyor
            video_file.save(os.path.join(UPLOAD_FOLDER, title_filename))

            # Yükleme başarılıysa ana sayfaya yönlendiriyoruz
            return redirect(url_for('main.home'))
    
    return render_template('upload.html')

# Video detay sayfası
@main.route('/video/<int:video_id>')
def video_detail(video_id):
    videos = get_uploaded_videos()
    video = next((v for v in videos if v['id'] == video_id), None)
    
    if video is None:
        return "Video bulunamadı", 404
    
    return render_template('video_detail.html', video=video)