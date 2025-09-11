from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import Article, Category, Match, BettingOdd
from . import db
from sqlalchemy import desc
from datetime import datetime, timedelta
from .seo_utils import generate_meta_tags

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
