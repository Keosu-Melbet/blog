from app import create_app, db

# Khởi tạo Flask app từ factory
app = create_app()

# Tạo bảng trong database nếu chưa có
with app.app_context():
    db.create_all()
    print("✅ Database initialized successfully")
