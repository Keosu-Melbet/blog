from app.models import Category
from app.extensions import db

categories = [
    {"name": "Soi Kèo", "slug": "soi-keo", "description": "Phân tích kèo bóng đá chuyên sâu"},
    {"name": "Mẹo Cược", "slug": "meo-cuoc", "description": "Kinh nghiệm cược từ cao thủ"},
    {"name": "Tin Tức", "slug": "tin-tuc", "description": "Cập nhật tin tức bóng đá mới nhất"},
    {"name": "Kèo Thơm", "slug": "keo-thom", "description": "Tổng hợp kèo thơm hôm nay"},
]

for cat in categories:
    if not Category.query.filter_by(slug=cat["slug"]).first():
        db.session.add(Category(**cat))

db.session.commit()
print("✅ Categories seeded")
