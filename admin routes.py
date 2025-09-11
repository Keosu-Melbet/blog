from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from functools import wraps
from app import db
from models import User, Article, Category
from forms import ArticleForm

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

# Middleware: kiểm tra quyền admin
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("admin.login"))
        user = User.query.get(session["user_id"])
        if not user or not user.is_admin:
            flash("Bạn không có quyền truy cập", "danger")
            return redirect(url_for("index"))
        return f(*args, **kwargs)
    return decorated_function


# Trang login admin
@admin_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password) and user.is_admin:
            session["user_id"] = user.id
            flash("Đăng nhập thành công!", "success")
            return redirect(url_for("admin.manage_articles"))
        flash("Sai tài khoản hoặc mật khẩu", "danger")
    return render_template("admin/login.html")


# Đăng xuất
@admin_bp.route("/logout")
def logout():
    session.pop("user_id", None)
    flash("Đã đăng xuất", "info")
    return redirect(url_for("admin.login"))


# Quản lý bài viết
@admin_bp.route("/articles")
@admin_required
def manage_articles():
    page = request.args.get("page", 1, type=int)
    articles = Article.query.order_by(Article.created_at.desc()).paginate(page=page, per_page=10)
    return render_template("admin/manage_articles.html", articles=articles)


# Tạo bài viết mới
@admin_bp.route("/create-article", methods=["GET", "POST"])
@admin_required
def create_article():
    form = ArticleForm()
    form.category_id.choices = [(c.id, c.name) for c in Category.query.all()]

    if form.validate_on_submit():
        article = Article(
            title=form.title.data,
            slug=form.title.data.lower().replace(" ", "-"),
            excerpt=form.excerpt.data,
            content=form.content.data,
            category_id=form.category_id.data,
            featured=form.featured.data,
            published=form.published.data,
        )
        db.session.add(article)
        db.session.commit()
        flash("Bài viết đã được tạo thành công!", "success")
        return redirect(url_for("admin.manage_articles"))

    return render_template("admin/create_article.html", form=form)


# (Tuỳ chọn) Sửa bài viết
@admin_bp.route("/edit-article/<int:article_id>", methods=["GET", "POST"])
@admin_required
def edit_article(article_id):
    article = Article.query.get_or_404(article_id)
    form = ArticleForm(obj=article)
    form.category_id.choices = [(c.id, c.name) for c in Category.query.all()]

    if form.validate_on_submit():
        form.populate_obj(article)
        db.session.commit()
        flash("Cập nhật bài viết thành công!", "success")
        return redirect(url_for("admin.manage_articles"))

    return render_template("admin/create_article.html", form=form, edit=True)


# (Tuỳ chọn) Xoá bài viết
@admin_bp.route("/delete-article/<int:article_id>", methods=["POST"])
@admin_required
def delete_article(article_id):
    article = Article.query.get_or_404(article_id)
    db.session.delete(article)
    db.session.commit()
    flash("Bài viết đã bị xoá", "warning")
    return redirect(url_for("admin.manage_articles"))
