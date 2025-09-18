from app.extensions import db
from datetime import datetime

# 🔹 Chuyên mục bài viết
class Category(db.Model):
    __tablename__ = "category"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False, index=True)
    description = db.Column(db.Text)

    articles = db.relationship("Article", backref="category", lazy=True)

    def __repr__(self):
        return f"<Category {self.name}>"

# 🔹 Bài viết
class Article(db.Model):
    __tablename__ = "article"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(255), unique=True, nullable=False, index=True)
    content = db.Column(db.Text, nullable=False)
    excerpt = db.Column(db.String(255))
    featured_image = db.Column(db.String(255))
    featured = db.Column(db.Boolean, default=False)
    published = db.Column(db.Boolean, default=False)
    views = db.Column(db.Integer, default=0)

    meta_title = db.Column(db.String(255))
    meta_description = db.Column(db.String(255))
    meta_keywords = db.Column(db.String(255))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    category_id = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=False)

    def generate_slug(self):
        return self.title.lower().replace(" ", "-")

    def get_excerpt(self, length=160):
        return self.content[:length] + "..." if len(self.content) > length else self.content

    def __repr__(self):
        return f"<Article {self.title}>"

# 🔹 Trận đấu bóng đá
class Match(db.Model):
    __tablename__ = "match"

    id = db.Column(db.Integer, primary_key=True)
    team_a = db.Column(db.String(100), nullable=False)
    team_b = db.Column(db.String(100), nullable=False)
    kickoff = db.Column(db.DateTime, nullable=False)

    odds = db.relationship("BettingOdd", backref="match", lazy=True)

    def __repr__(self):
        return f"<Match {self.team_a} vs {self.team_b}>"

# 🔹 Tỷ lệ cược
class BettingOdd(db.Model):
    __tablename__ = "betting_odd"

    id = db.Column(db.Integer, primary_key=True)
    match_id = db.Column(db.Integer, db.ForeignKey("match.id"), nullable=False)
    odd_type = db.Column(db.String(50), nullable=False)
    value = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<Odd {self.odd_type}: {self.value}>"
