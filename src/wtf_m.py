from wtforms import StringField, SubmitField, PasswordField, EmailField, BooleanField, validators, IntegerField
from flask_wtf import FlaskForm


class Add_Group_Form(FlaskForm):
    group_name = StringField('Название группы', validators=[validators.DataRequired()])
    tuitor_name = StringField('Имя преподавателя:', validators=[validators.DataRequired()])
    submit = SubmitField('Исполнить')