from flask import render_template, request, redirect, url_for, session, flash
from werkzeug.utils import secure_filename
import os
from app import app, db
from models import User, Article, Category

# ---- Auth ----
@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session["admin_id"] = user.id
            return redirect(url_for("admin_dashboard"))
        flash("Sai tài khoản hoặc mật khẩu", "danger")
    return render_template("admin/login.html")

@app.route("/admin/logout")
def admin_logout():
    session.pop("admin_id", None)
    return redirect(url_for("index"))

def login_required(f):
    def wrapper(*args, **kwargs):
        if "admin_id" not in session:
            return redirect(url_for("admin_login"))
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

# ---- Dashboard ----
@app.route("/admin")
@login_required
def admin_dashboard():
    return render_template("admin/dashboard.html")

@app.route("/admin/articles")
@login_required
def manage_articles():
    articles = Article.query.all()
    return render_template("admin/manage_articles.html", articles=articles)

@app.route("/admin/articles/create", methods=["GET", "POST"])
@login_required
def create_article():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        category_id = request.form.get("category")

        # Upload ảnh
        image_file = request.files.get("featured_image")
        image_path = None
        if image_file:
            filename = secure_filename(image_file.filename)
            upload_folder = os.path.join("static", "uploads")
            os.makedirs(upload_folder, exist_ok=True)
            filepath = os.path.join(upload_folder, filename)
            image_file.save(filepath)
            image_path = f"uploads/{filename}"

        article = Article(
            title=title,
            content=content,
            slug=title.lower().replace(" ", "-"),
            category_id=category_id,
            author_id=session["admin_id"],
            featured_image=image_path,
        )
        db.session.add(article)
        db.session.commit()
        return redirect(url_for("manage_articles"))

    categories = Category.query.all()
    return render_template("admin/create_article.html", categories=categories)
