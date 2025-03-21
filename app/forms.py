from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class RegistrationForm(FlaskForm):
    username = StringField('用户名', validators=[
        DataRequired(),
        Length(min=2, max=64)
    ])
    email = StringField('邮箱', validators=[
        DataRequired(),
        Email()
    ])
    submit = SubmitField('注册')
