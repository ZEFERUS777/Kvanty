from flask import Flask, render_template, request, flash, redirect, url_for
from src.models import db, Groups, Students
from src.wtf_m import Add_Group_Form, Add_Student_Form


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///kvant.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "sapperboy"
db.init_app(app)


@app.route('/')
@app.route("/index")
def index():
    return render_template("base.html")


@app.route("/groups")
def groups():
    group = Groups.query.all()
    print(group)
    return render_template("groups.html", groups=group)


@app.route("/add_group", methods=["GET", "POST"])
def add_group():
    form = Add_Group_Form()
    if request.method == "POST":
        group = Groups(group_name=form.group_name.data,
                       tuitor=form.tuitor_name.data)
        db.session.add(group)
        db.session.commit()
        return render_template("add_group.html", form=form)
    return render_template("add_group.html", form=form)


@app.route("/group/<string:id>", methods=["GET", "POST"])
def group(id):
    group = Groups.query.get(int(id))
    if request.method == "POST":
        student_name = request.form.get("student_name")
        students = group.Students.split(",") if group.Students else []
        if student_name.strip() in students:
            flash("Студент уже записан", "warning")
            return redirect(url_for("group", id=id))
        students.append(student_name.strip())
        group.Students = ",".join(students)
        db.session.commit()
        flash("Вы записались", "success")
    return render_template("group.html", group=group)


@app.route("/grau/<int:id>", methods=["GET", "POST"])
def group_detail(id):
    group = Groups.query.get_or_404(id)
    form = Add_Student_Form()

    if form.validate_on_submit():
        try:
            students_list = group.Students.split(",") if group.Students else []

            new_student = f"{form.student_name.data.strip()}"
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
                           students=group.Students.split(",") if group.Students else [])


with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)
