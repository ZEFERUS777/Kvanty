from flask import Flask, render_template, request
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


with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run()
    