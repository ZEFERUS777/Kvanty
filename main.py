from flask import Flask, render_template, request, flash, redirect, url_for
from src.models import db, Groups, Students, Users
from src.wtf_m import Add_Group_Form, Add_Student_Form, LoginForm, RegistrationForm
from flask_login import LoginManager, login_user, logout_user, current_user, login_required


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///kvant.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "sapperboy"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

db.init_app(app)


@app.route('/')
@app.route("/index")
def index():
    # Для незарегистрированных пользователей
    if not current_user.is_authenticated:
        return render_template("base.html")

    # Для зарегистрированных пользователей
    if current_user.rule == 1:
        return render_template("base.html", rule="admin", autorized=True)
    else:
        return render_template("base.html", autorized=True)


@app.route("/groups")
@login_required
def groups():
    group = Groups.query.all()
    return render_template("groups.html", groups=group, autorized=True)


@app.route("/add_group", methods=["GET", "POST"])
@login_required
def add_group():
    if current_user.rule == 1:
        form = Add_Group_Form()
        if request.method == "POST":
            group = Groups(group_name=form.group_name.data,
                           tuitor=form.tuitor_name.data)
            db.session.add(group)
            db.session.commit()
            return render_template("add_group.html", form=form)
        return render_template("add_group.html", form=form)
    else:
        flash("У вас нет прав для добавления группы", "error")
        return redirect(url_for("groups"))


@app.route("/group/<string:id>", methods=["GET", "POST"])
@login_required
def group(id):
    group = Groups.query.get(int(id))
    lead = group.lead_id
    students = Users.query.filter_by(group_id=id, rule=0).all()
    if not lead and current_user.rule == 1:
        return render_template("group.html", group=group, lead=True, autorized=True)
    if request.method == "POST":
        student_name = request.form.get("student_name")
        students = Users.query.filter_by(username=student_name).all()
        if student_name.strip() in students:
            flash("Студент уже записан", "warning")
            return redirect(url_for("group", id=id))
        students.append(student_name.strip())
        group.Students = ",".join(students)
        db.session.commit()
        flash("Вы записались", "success")
    return render_template("group.html", group=group, user=current_user, students=students,
                           autorized=True)


# функция для для записи ученика в группу
@app.route("/grau/<int:id>", methods=["GET", "POST"])
@login_required
def group_detail(id):
    group = Groups.query.get_or_404(id)
    users = Users.query.all()
    students = Users.query.filter_by(group_id=id, rule=0).all()
    
    if current_user.id != group.lead_id:
        flash("Вы не являетесь руководителем этой группы", "error")
        return redirect(url_for("groups"))

    form = Add_Student_Form()

    if form.validate_on_submit():
        try:
            students_list = group.Students.split(",") if group.Students else []

            new_student = f"{form.student_name.data.strip()}"
            user = Users.query.filter_by(username=new_student).first()
            user.group_id = group.id
            if new_student:
                students_list.append(new_student)

                group.Students = ",".join(students_list)
                db.session.commit()
                flash("Студент успешно добавлен", "success")
                new_student = Students(
                    name=form.student_name.data, group_id=id)
                db.session.add(new_student)
                db.session.commit()
                return redirect(url_for("group_detail", id=id))

        except Exception as e:
            db.session.rollback()
            flash(f"Ошибка при добавлении: {str(e)}", "error")

    return render_template("add_student.html",
                           form=form,
                           group=group,
                           autorized=True,
                           users=users,
                           students=students)


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(Users, user_id)


@app.route("/login", methods=["GET", "POST"])
def login():
    login_form = LoginForm()
    if request.method == "POST":
        email = login_form.email.data
        password = login_form.password.data
        try:
            user = Users.query.filter_by(email=email).first()
            if user and user.check_password(password):
                login_user(user)
                return redirect(url_for("index"))
            else:
                return render_template("login.html", form=login_form,
                                       error="Неверный логин или пароль")
        except Exception:
            return render_template("login.html", form=login_form, error="Ошибка при входе")
    return render_template("login.html", form=login_form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if request.method == "POST":
        name = form.name.data
        surname = form.surname.data
        email = form.email.data
        password = form.password.data
        user_login = name + " " + surname
        try:
            if Users.query.filter_by(email=email).first():
                return render_template("register.html", form=form, error="Пользователь с такой почтой уже зарегистрирован")
            if Users.query.filter_by(username=user_login).first():
                return render_template("register.html", form=form, error="Пользователь с таким логином уже существует")
            new_user = Users(username=user_login, email=email,
                            rule=0, group_rate=0)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for("login"))
        except Exception:
            return render_template("register.html", form=form, error="Ошибка при регистрации")
    return render_template("register.html", form=form)


@app.route("/set_lead/<int:id>", methods=["GET", "POST"])
@login_required
def set_lead(id):
    if current_user.rule != 1:  # Исправлено сравнение
        flash("У вас нет прав для назначения руководителя", "error")
        return redirect(url_for("groups"))

    group = Groups.query.get_or_404(id)
    users = Users.query.filter_by(rule=3).all()

    if request.method == "POST":
        new_lead_id = request.form.get("lead_id")

        if not new_lead_id:
            flash("Не выбран руководитель", "error")
            return redirect(url_for("set_lead", id=id))

        user = Users.query.get(new_lead_id)

        if not user:
            flash("Пользователь не найден", "error")
            return redirect(url_for("set_lead", id=id))

        # Снимаем предыдущую роль лидера если нужно
        prev_lead = Users.query.get(group.lead_id)
        if prev_lead:
            prev_lead.rule = 3  # Возвращаем роль учителя

        # Назначаем нового лидера
        user.lead_group = group.id
        group.lead_id = user.id
        user.group_id = group.id
        db.session.commit()

        flash("Руководитель группы успешно назначен!", "success")
        return redirect(url_for("groups"))

    return render_template("set_lead.html", group=group, teachers=users, autorized=True)


# роут для назначения администратора
@login_required
@app.route("/get_adm")
def get_adm():
    user = Users.query.filter_by(id=current_user.id).first()
    user.rule = 1
    db.session.commit()
    return redirect(url_for("groups"))


@app.route("/set_teacher", methods=["GET", "POST"])
@login_required
def set_teacher():
    if current_user.rule != 1:  # Исправлено сравнение
        flash("У вас нет прав для назначения руководителя", "error")
        return redirect(url_for("groups"))
    users = Users.query.filter_by(rule=0).all()
    if request.method == "POST":
        teacher_id = request.form.get("teacher_id")
        user = Users.query.get(teacher_id)
        if user:
            user.rule = 3
            db.session.commit()
            flash("Учитель успешно назначен!", "success")
            return redirect(url_for("index"))
        else:
            return render_template("set_teacher.html", teachers=users, error="Пользователь не найден", autorized=True)
    return render_template("set_teacher.html", teachers=users, autorized=True)


@app.route("/student/<int:id>", methods=["GET", "POST"])
@login_required
def student(id):
    student = Users.query.get_or_404(id)
    group = Groups.query.filter_by(id=student.group_id).first()

    if current_user.lead_group != group.id:
        flash("У вас нет прав для просмотра этого студента", "error")
        return redirect(url_for("index"))

    if request.method == "POST":
        try:
            rat = int(request.form.get("rating", 0))
            if rat < 0 or rat > 100:
                flash("Оценка должна быть от 0 до 100", "error")
                return redirect(url_for("student", id=id))

            student.group_rate = rat
            db.session.commit()
            flash("Оценка успешно обновлена", "success")
        except ValueError:
            flash("Некорректное значение оценки", "error")

        return redirect(url_for("student", id=id))

    rate = student.group_rate or 0
    return render_template("student.html", student=student, rate=rate, group=group, autorized=True)


@app.route("/profile")
@login_required
def profile():
    group = Groups.query.filter_by(id=current_user.group_id).first()
    if current_user.rule == 1:
        return render_template("profile.html", user=current_user, group=group, autorized=True, rule="admin")
    else:
        return render_template("profile.html", user=current_user, group=group, autorized=True)
    
    
@app.route("/group_rate/<int:id>")
@login_required
def group_rate(id):
    if id != current_user.group_id:
        flash("У вас нет прав для просмотра этого рейтинга", "error")
        return redirect(url_for("index"))
    group = Groups.query.get_or_404(id)
    students = Users.query.filter_by(group_id=id, rule=0).order_by(Users.group_rate).all()
    return render_template("rate_list.html", students=students, group=group, autorized=True, user=current_user)

with app.app_context():
    db.create_all()


if __name__ == "__main__":
    print("Запуск сервера")
    app.run(debug=True)
