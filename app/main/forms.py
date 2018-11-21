from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class SearchForm(FlaskForm):
    keyword = StringField('请输入关键字', validators=[DataRequired()])
    submit = SubmitField('搜索')