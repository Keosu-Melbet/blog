from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SelectField
from wtforms.validators import DataRequired

class ArticleForm(FlaskForm):
    title = StringField("Tiêu đề", validators=[DataRequired()])
    content = TextAreaField("Nội dung", validators=[DataRequired()])
    category_id = SelectField("Danh mục", choices=[], coerce=int)
    published = BooleanField("Công khai")

class ContactForm(FlaskForm):
    name = StringField("Tên", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    message = TextAreaField("Tin nhắn", validators=[DataRequired()])

class SearchForm(FlaskForm):
    keyword = StringField("Từ khóa", validators=[DataRequired()])
