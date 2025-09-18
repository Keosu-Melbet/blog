from flask import Blueprint, render_template, redirect, url_for, flash, request
from .models import Article, Category
from .forms import ArticleForm
from . import db
from sqlalchemy import desc

admin_bp = Blueprint("admin", __name__, template_folder="templates/admin")

# ✅ Trang dashboard admin
@admin_bp.route("/", endpoint="dashboard")
def dashboard():
    return render_template("admin/dashboard.html")

# ✅ Quản lý bài viết
@admin_bp.route("/articles", endpoint="manage_articles")
def manage_articles():
    page = request.args.get("page", 1, type=int)
    articles = Article.query.order_by(desc(Article.created_at))\
                            .paginate(page=page, per_page=20, error_out=False)
    return render_template("admin/manage_articles.html", articles=articles)

# ✅ Tạo bài viết mới
@admin_bp.route("/articles/create", methods=["GET", "POST"], endpoint="create_article")
def create_article():
    form = ArticleForm()
    form.category_id.choices = [(c.id, c.name) for c in Category.query.order_by(Category.name).all()]

    if form.validate_on_submit():
        # Tạo excerpt nếu chưa nhập
        excerpt = form.excerpt.data or form.content.data[:160]

        article = Article(
            title=form.title.data,
            content=form.content.data,
            category_id=form.category_id.data,
            excerpt=excerpt,
            featured_image=form.featured_image.data,
            published=form.published.data,
            featured=form.featured.data,
            meta_title=form.meta_title.data or form.title.data,
            meta_description=form.meta_description.data or excerpt,
            meta_keywords=form.meta_keywords.data
        )
        article.slug = article.generate_slug()

        db.session.add(article)
        db.session.commit()
        flash("✅ Bài viết đã được tạo!", "success")
        return redirect(url_for("admin.manage_articles"))

    return render_template("admin/create_article.html", form=form)


