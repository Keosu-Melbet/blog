from flask import Blueprint, render_template, request, redirect, url_for, flash, make_response
from .models import Article, Category, Match, BettingOdd
from .forms import ContactForm, SearchForm
from . import db
from .seo_utils import generate_meta_tags
from sqlalchemy import desc, or_
from datetime import datetime, timedelta

main_bp = Blueprint("main", __name__)

# Trang chủ
@main_bp.route("/")
def index():
    featured_articles = Article.query.filter_by(published=True, featured=True).limit(3).all()
    recent_articles = Article.query.filter_by(published=True).order_by(desc(Article.created_at)).limit(6).all()
    meta_tags = generate_meta_tags(
        title="Kèo Sư - Website Kèo Bóng Đá Chuyên Nghiệp",
        description="Kèo Sư cung cấp tỷ lệ kèo, soi kèo, mẹo cược bóng đá chính xác.",
        keywords="kèo bóng đá, soi kèo, mẹo cược"
    )
    return render_template("index.html", featured_articles=featured_articles, recent_articles=recent_articles, meta_tags=meta_tags)

# Kèo thơm
@main_bp.route("/keo-thom")
def keo_thom():
    today = datetime.now().date()
    odds = BettingOdd.query.filter(BettingOdd.match_date == today).all()
    meta_tags = generate_meta_tags(
        title="Kèo Thơm Hôm Nay",
        description="Cập nhật kèo thơm hôm nay từ các nhà cái uy tín.",
        keywords="kèo thơm, tỷ lệ kèo"
    )
    return render_template("keo-thom.html", odds=odds, meta_tags=meta_tags)

# Mẹo cược
@main_bp.route("/meo-cuoc")
@main_bp.route("/meo-cuoc/page/<int:page>")
def meo_cuoc(page=1):
    category = Category.query.filter_by(slug="meo-cuoc").first_or_404()
    articles = Article.query.filter_by(category_id=category.id, published=True).order_by(desc(Article.created_at)).paginate(page=page, per_page=10)
    meta_tags = generate_meta_tags(
        title="Mẹo Cược Bóng Đá",
        description="Chia sẻ mẹo cược bóng đá hiệu quả từ chuyên gia.",
        keywords="mẹo cược, cá độ bóng đá"
    )
    return render_template("meo-cuoc.html", articles=articles, category=category, meta_tags=meta_tags)
    
@main_bp.route("/soi-keo")
@main_bp.route("/soi-keo/page/<int:page>")
def soi_keo(page=1):
    category = Category.query.filter_by(slug="soi-keo").first_or_404()
    articles = Article.query.filter_by(category_id=category.id, published=True)\
        .order_by(desc(Article.created_at))\
        .paginate(page=page, per_page=10)
    
    meta_tags = generate_meta_tags(
        title="Soi Kèo Bóng Đá | Kèo Sư",
        description="Phân tích kèo bóng đá hôm nay từ chuyên gia Kèo Sư.",
        keywords="soi kèo, kèo bóng đá"
    )
    
    return render_template("soi-keo.html", articles=articles, category=category, meta_tags=meta_tags)


# Đại lý MelBet
@main_bp.route("/dai-ly-melbet")
def dai_ly_melbet():
    meta_tags = generate_meta_tags(
        title="Đại Lý MelBet",
        description="Tham gia chương trình affiliate MelBet với hoa hồng cao.",
        keywords="MelBet, affiliate, đại lý cá cược"
    )
    return render_template("dai-ly-melbet.html", meta_tags=meta_tags)

# Liên hệ
@main_bp.route("/lien-he", methods=["GET", "POST"])
def lien_he():
    form = ContactForm()
    if form.validate_on_submit():
        flash("Cảm ơn bạn đã liên hệ!", "success")
        return redirect(url_for("main.lien_he"))
    meta_tags = generate_meta_tags(
        title="Liên Hệ",
        description="Liên hệ với Kèo Sư để được tư vấn và hỗ trợ.",
        keywords="liên hệ, tư vấn kèo"
    )
    return render_template("lien-he.html", form=form, meta_tags=meta_tags)

# Chi tiết bài viết
@main_bp.route("/bai-viet/<slug>")
def article_detail(slug):
    article = Article.query.filter_by(slug=slug, published=True).first_or_404()
    article.views += 1
    db.session.commit()
    related_articles = Article.query.filter(
        Article.category_id == article.category_id,
        Article.id != article.id,
        Article.published == True
    ).limit(3).all()
    meta_tags = generate_meta_tags(
        title=article.meta_title or article.title,
        description=article.meta_description or article.get_excerpt(160),
        keywords=article.meta_keywords or f"{article.title}, {article.category.name}"
    )
    return render_template("article.html", article=article, related_articles=related_articles, meta_tags=meta_tags)

# Chuyên mục
@main_bp.route("/chuyen-muc/<slug>")
@main_bp.route("/chuyen-muc/<slug>/page/<int:page>")
def category_articles(slug, page=1):
    category = Category.query.filter_by(slug=slug).first_or_404()
    articles = Article.query.filter_by(category_id=category.id, published=True).order_by(desc(Article.created_at)).paginate(page=page, per_page=10)
    meta_tags = generate_meta_tags(
        title=f"{category.name} | Kèo Sư",
        description=category.description or f"Tất cả bài viết về {category.name}",
        keywords=f"{category.name}, {category.slug}"
    )
    return render_template("category.html", category=category, articles=articles, meta_tags=meta_tags)

# Tìm kiếm
@main_bp.route("/search")
def search():
    query = request.args.get("q", "")
    page = request.args.get("page", 1, type=int)
    if query:
        articles = Article.query.filter(
            or_(
                Article.title.contains(query),
                Article.content.contains(query)
            ),
            Article.published == True
        ).order_by(desc(Article.created_at)).paginate(page=page, per_page=10)
    else:
        articles = Article.query.filter_by(published=False).paginate(page=1, per_page=0)
    meta_tags = generate_meta_tags(
        title=f"Tìm kiếm: {query} | Kèo Sư" if query else "Tìm kiếm | Kèo Sư",
        description=f"Kết quả tìm kiếm cho '{query}'" if query else "Tìm kiếm bài viết",
        keywords=f"tìm kiếm, {query}" if query else "tìm kiếm"
    )
    return render_template("search.html", articles=articles, query=query, meta_tags=meta_tags)

# Sitemap
@main_bp.route("/sitemap.xml")
def sitemap():
    pages = []
    static_pages = [
        {"url": url_for("main.index"), "priority": "1.0"},
        {"url": url_for("main.keo_thom"), "priority": "0.9"},
        {"url": url_for("main.meo_cuoc"), "priority": "0.8"},
        {"url": url_for("main.dai_ly_melbet"), "priority": "0.6"},
        {"url": url_for("main.lien_he"), "priority": "0.5"},
    ]
    articles = Article.query.filter_by(published=True).all()
    for article in articles:
        pages.append({
            "url": url_for("main.article_detail", slug=article.slug),
            "lastmod": article.updated_at.strftime("%Y-%m-%d"),
            "priority": "0.8"
        })
    categories = Category.query.all()
    for category in categories:
        pages.append({
            "url": url_for("main.category_articles", slug=category.slug),
            "priority": "0.6"
        })
    pages.extend(static_pages)
    response = make_response(render_template("sitemap.xml", pages=pages))
    response.headers["Content-Type"] = "application/xml"
    return response

# Robots.txt
@main_bp.route("/robots.txt")
def robots():
    response = make_response(render_template("robots.txt"))
    response.headers["Content-Type"] = "text/plain"
    return response

# Error handlers
@main_bp.app_errorhandler(404)
def not_found_error(error):
    meta_tags = generate_meta_tags(
        title="404 - Không tìm thấy",
        description="Trang bạn tìm kiếm không tồn tại.",
        keywords="404, lỗi trang"
    )
    return render_template("404.html", meta_tags=meta_tags), 404

@main_bp.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    meta_tags = generate_meta_tags(
        title="500 - Lỗi hệ thống",
        description="Đã xảy ra lỗi hệ thống.",
        keywords="500, lỗi server"
    )
    return render_template("500.html", meta_tags=meta_tags), 500

# Inject global variables
@main_bp.context_processor
def inject_globals():
    categories = Category.query.all()
    search_form = SearchForm()
    return {"categories": categories, "search_form": search_form}
