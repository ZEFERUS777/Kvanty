from flask import Flask, render_template, request, flash, redirect, url_for
from src.models import db, Groups
from src.wtf_m import Add_Group_Form


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
        group = Groups(group_name=form.group_name.data, tuitor=form.tuitor_name.data)
        db.session.add(group)
        db.session.commit()
        return render_template("add_group.html", form=form)
    return render_template("add_group.html", form=form)


# app.py (обновленный роут)
@app.route("/group/<string:id>", methods=["GET", "POST"])
def group(id):
    group = Groups.query.get(int(id))
    if request.method == "POST":
        student_name = request.form.get("student_name")
        # Разделение строки в список
        students = group.Students.split(",") if group.Students else []
        if student_name.strip() in students:
            flash("Студент уже записан", "warning")
            return redirect(url_for("group", id=id))
        students.append(student_name.strip())
        group.Students = ",".join(students)  # Объединение обратно в строку
        db.session.commit()
        flash("Вы записались", "success")
    return render_template("group.html", group=group)
    


with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run()
    