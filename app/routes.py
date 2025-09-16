from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import Article, Category, Match, BettingOdd
from . import db
from sqlalchemy import desc
from .seo_utils import generate_meta_tags
from .forms import ContactForm, SearchForm

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def index():
    featured_articles = Article.query.filter_by(published=True, featured=True).limit(3).all()
    recent_articles = Article.query.filter_by(published=True).order_by(desc(Article.created_at)).limit(6).all()

    meta_tags = generate_meta_tags(
        title="Kèo Sư - Website Kèo Bóng Đá Chuyên Nghiệp",
        description="Kèo Sư cung cấp tỷ lệ kèo, soi kèo, mẹo cược bóng đá chính xác.",
        keywords="kèo bóng đá, soi kèo, mẹo cược"
    )
    return render_template("index.html",
                           featured_articles=featured_articles,
                           recent_articles=recent_articles,
                           meta_tags=meta_tags)

@main_bp.route("/soi-keo")
def soi_keo():
    articles = Article.query.filter_by(published=True).order_by(desc(Article.created_at)).limit(10).all()
    category = Category.query.filter_by(name="Soi Kèo").first()

    meta_tags = generate_meta_tags(
        title="Soi Kèo Bóng Đá",
        description="Phân tích kèo bóng đá hôm nay",
        keywords="soi kèo, kèo bóng đá"
    )
    return render_template("soi-keo.html",
                           articles=articles,
                           category=category,
                           meta_tags=meta_tags)

@main_bp.route("/meo-cuoc")               
def meo_cuoc():
    articles = Article.query.filter_by(published=True).order_by(desc(Article.created_at)).limit(10).all()
    category = Category.query.filter_by(name="Mẹo Cược").first()

    meta_tags = generate_meta_tags(
        title="Mẹo Cược Bóng Đá",
        description="Tổng hợp mẹo cược bóng đá hiệu quả",
        keywords="mẹo cược, mẹo cá độ"
    )
    return render_template("meo-cuoc.html",
                           articles=articles,
                           category=category,
                           meta_tags=meta_tags)

@main_bp.route("/tin-tuc")
@main_bp.route("/tin-tuc/<category>")
def tin_tuc(category=None):
    query = Article.query.filter_by(published=True)

    if category:
        cat = Category.query.filter_by(slug=category).first()
        if cat:
            query = query.filter_by(category_id=cat.id)

    page = request.args.get("page", 1, type=int)
    articles = query.order_by(desc(Article.created_at)).paginate(page=page, per_page=10)

    meta_tags = generate_meta_tags(
        title="Tin Tức Bóng Đá",
        description="Cập nhật tin tức bóng đá mới nhất",
        keywords="tin tức bóng đá, tin thể thao"
    )

    return render_template("tin-tuc.html", articles=articles, meta_tags=meta_tags)

@main_bp.route("/lien-he", methods=["GET", "POST"])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        flash("Cảm ơn bạn đã liên hệ!", "success")
        return redirect(url_for("main.contact"))

    # ✅ Thêm meta_tags tại đây
    meta_tags = generate_meta_tags(
        title="Liên Hệ Kèo Sư",
        description="Gửi liên hệ, góp ý hoặc hợp tác với Kèo Sư. Chúng tôi luôn sẵn sàng hỗ trợ.",
        keywords="liên hệ, hỗ trợ, tư vấn kèo bóng đá"
    )

    return render_template("contact.html", form=form, meta_tags=meta_tags)

@main_bp.route("/tim-kiem", methods=["GET", "POST"])
def search():
    form = SearchForm()
    results = []
    if form.validate_on_submit():
        keyword = form.keyword.data
        results = Article.query.filter(Article.title.ilike(f"%{keyword}%")).all()
    return render_template("search.html", form=form, results=results)
