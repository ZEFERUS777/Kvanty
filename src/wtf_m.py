from wtforms import StringField, SubmitField, PasswordField, EmailField, BooleanField, validators, IntegerField
from flask_wtf import FlaskForm


class Add_Group_Form(FlaskForm):
    group_name = StringField('Название группы', validators=[
                             validators.DataRequired()])
    tuitor_name = StringField('Имя преподавателя:', validators=[
                              validators.DataRequired()])
    submit = SubmitField('Исполнить')


class StudentForm(FlaskForm):
    student_name = StringField('ФИО', [validators.DataRequired()])


class Add_Student_Form(FlaskForm):
    student_name = StringField('ФИО студента', validators=[
                               validators.DataRequired()])
    submit = SubmitField('Записаться')


class LoginForm(FlaskForm):
    email = EmailField('Введите ваш email', validators=[validators.DataRequired()])
    password = PasswordField('Введите ваш пароль', validators=[validators.DataRequired()])
    remember = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')
    

class RegistrationForm(FlaskForm):
    name = StringField('Введите ваше имя:', validators=[validators.DataRequired()])
    surname = StringField('Введите вашу фамилию:', validators=[validators.DataRequired()])
    email = StringField('Введите ваш email:', validators=[validators.DataRequired()])
    password = PasswordField('Введите ваш пароль:', validators=[validators.DataRequired()])