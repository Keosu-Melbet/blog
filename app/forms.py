from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email

class ArticleForm(FlaskForm):
    title = StringField("Tiêu đề", validators=[DataRequired()])
    content = TextAreaField("Nội dung", validators=[DataRequired()])
    category = SelectField("Nhóm danh mục", choices=[], validators=[DataRequired()])
    published = BooleanField("Có hiển thị")

class ContactForm(FlaskForm):
    name = StringField("Họ và tên", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    subject = StringField("Tiêu đề", validators=[DataRequired()])
    message = TextAreaField("Nội dung", validators=[DataRequired()])
    submit = SubmitField("Gửi liên hệ")

class SearchForm(FlaskForm):
    keyword = StringField("Từ khóa", validators=[DataRequired()])
