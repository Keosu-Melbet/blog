from flask import Blueprint, render_template, redirect, url_for, flash, request
from .models import Article
from .forms import ArticleForm
from . import db
from sqlalchemy import desc

admin_bp = Blueprint("admin", __name__, template_folder="templates/admin")

@admin_bp.route("/")
def dashboard():
    return render_template("admin/dashboard.html")

@admin_bp.route("/articles")
def manage_articles():
    page = request.args.get("page", 1, type=int)
    articles = Article.query.order_by(desc(Article.created_at))\
                            .paginate(page=page, per_page=20, error_out=False)
    return render_template("admin/manage_articles.html", articles=articles)

@admin_bp.route("/articles/create", methods=["GET", "POST"])
def create_article():
    form = ArticleForm()
    if form.validate_on_submit():
        article = Article(
            title=form.title.data,
            content=form.content.data,
            category_id=form.category_id.data,
            published=form.published.data
        )
        article.slug = article.generate_slug()
        db.session.add(article)
        db.session.commit()
        flash("Bài viết đã được tạo!", "success")
        return redirect(url_for("admin.manage_articles"))
    return render_template("admin/create_article.html", form=form)
