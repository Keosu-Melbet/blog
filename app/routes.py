from flask import Blueprint, render_template, request, redirect, url_for, flash, make_response
from .models import Article, Category, Match, BettingOdd
from .forms import ContactForm, SearchForm
from . import db
from .seo_utils import generate_meta_tags
from sqlalchemy import desc, or_
from datetime import datetime
from sqlalchemy.orm import joinedload

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
    odds = BettingOdd.query.join(Match).filter(
        db.func.date(Match.kickoff) == today
    ).options(joinedload(BettingOdd.match)).all()

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

# Soi kèo
@main_bp.route("/soi-keo")
@main_bp.route("/soi-keo/page/<int:page>")
def soi_keo(page=1):
    category = Category.query.filter_by(slug="soi-keo").first_or_404()
    articles = Article.query.filter_by(category_id=category.id, published=True).order_by(desc(Article.created_at)).paginate(page=page, per_page=10)
    meta_tags = generate_meta_tags(
        title="Soi Kèo Bóng Đá | Kèo Sư",
        description="Phân tích kèo bóng đá hôm nay từ chuyên gia Kèo Sư.",
        keywords="soi kèo, kèo bóng đá"
    )
    return render_template("soi-keo.html", articles=articles, category=category, meta_tags=meta_tags)

# Tin tức
@main_bp.route("/tin-tuc")
@main_bp.route("/tin-tuc/page/<int:page>")
def tin_tuc(page=1):
    category = Category.query.filter_by(slug="tin-tuc").first_or_404()
    articles = Article.query.filter_by(category_id=category.id, published=True).order_by(desc(Article.created_at)).paginate(page=page, per_page=10)
    meta_tags = generate_meta_tags(
        title="Tin Tức Bóng Đá | Kèo Sư",
        description="Cập nhật tin tức bóng đá mới nhất từ các giải đấu lớn.",
        keywords="tin tức bóng đá, tin thể thao"
    )
    return render_template("tin-tuc.html", articles=articles, category=category, meta_tags=meta_tags)
    
# Lịch thi đấu
@main_bp.route("/lich-thi-dau")
def lich_thi_dau():
    selected_date = request.args.get("date", datetime.now().date().strftime("%Y-%m-%d"))
    matches = Match.query.filter(
        db.func.date(Match.kickoff) == selected_date
    ).all()
    meta_tags = generate_meta_tags(
        title="Lịch Thi Đấu Bóng Đá",
        description="Lịch thi đấu các giải bóng đá hàng đầu thế giới.",
        keywords="lịch thi đấu, bóng đá"
    )
    return render_template("lich-thi-dau.html", matches=matches, selected_date=selected_date, meta_tags=meta_tags)

    
# Tỷ số trực tiếp
@main_bp.route("/ty-so-truc-tiep")
def ty_so_truc_tiep():
    sample_matches = [
        {"league": "Premier League", "time": "21:00", "team_a": "Man United", "team_b": "Arsenal", "status": "LIVE", "status_color": "danger", "score": "2 - 1"},
        {"league": "La Liga", "time": "22:30", "team_a": "Real Madrid", "team_b": "Barcelona", "status": "FT", "status_color": "success", "score": "3 - 1"},
        {"league": "Serie A", "time": "23:45", "team_a": "Juventus", "team_b": "AC Milan", "status": "HT", "status_color": "warning", "score": "1 - 0"},
    ]
    features = [
        {"icon": "fas fa-bolt", "title": "Cập Nhật Nhanh", "description": "Tỷ số cập nhật realtime từ sân đấu"},
        {"icon": "fas fa-globe", "title": "Toàn Cầu", "description": "Theo dõi các giải đấu trên thế giới"},
        {"icon": "fas fa-chart-bar", "title": "Thống Kê", "description": "Thông tin chi tiết về từng trận đấu"},
        {"icon": "fas fa-mobile-alt", "title": "Mobile Friendly", "description": "Xem trên mọi thiết bị dễ dàng"},
    ]
    return render_template("ty-so-truc-tiep.html", sample_matches=sample_matches, features=features)

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

# Chuyên mục động
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
    query = request.args.get("q", "").strip()
    page = request.args.get("page", 1, type=int)

    if query:
        articles = Article.query.filter(
            or_(
                Article.title.ilike(f"%{query}%"),
                Article.content.ilike(f"%{query}%")
            ),
            Article.published == True
        ).order_by(desc(Article.created_at)).paginate(page=page, per_page=10)
    else:
        articles = None  # Không hiển thị kết quả nếu không có từ khóa

    meta_tags = generate_meta_tags(
        title=f"Tìm kiếm: {query} | Kèo Sư" if query else "Tìm kiếm | Kèo Sư",
        description=f"Kết quả tìm kiếm cho '{query}'" if query else "Tìm kiếm bài viết",
        keywords=f"tìm kiếm, {query}" if query else "tìm kiếm"
    )

    return render_template("search.html", articles=articles, query=query, meta_tags=meta_tags)
