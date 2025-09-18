from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, Optional

# Form tạo bài viết (đã tích hợp đầy đủ)
class ArticleForm(FlaskForm):
    title = StringField("Tiêu đề", validators=[DataRequired()])
    category_id = SelectField("Chuyên mục", coerce=int, choices=[], validators=[DataRequired()])
    content = TextAreaField("Nội dung", validators=[DataRequired()])
    excerpt = TextAreaField("Mô tả ngắn", validators=[Optional()])
    featured_image = StringField("Ảnh đại diện", validators=[Optional()])
    published = BooleanField("Xuất bản")
    featured = BooleanField("Nổi bật")
    meta_title = StringField("Meta Title", validators=[Optional()])
    meta_keywords = StringField("Meta Keywords", validators=[Optional()])
    meta_description = TextAreaField("Meta Description", validators=[Optional()])
    submit = SubmitField("Lưu bài viết")

# Form liên hệ
class ContactForm(FlaskForm):
    name = StringField("Họ và tên", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    subject = StringField("Tiêu đề", validators=[DataRequired()])
    message = TextAreaField("Nội dung", validators=[DataRequired()])
    submit = SubmitField("Gửi liên hệ")

# Form tìm kiếm
class SearchForm(FlaskForm):
    keyword = StringField("Từ khóa", validators=[DataRequired()])
    submit = SubmitField("Tìm kiếm")
