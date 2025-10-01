import os
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

# Prefer DATABASE_URL provided by Render Postgres
database_url = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)


# Flask 3.0 では before_first_request が非推奨のため起動時に作成
with app.app_context():
    db.create_all()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/greet", methods=["POST"])
def greet():
    name = request.form.get("name", "名無し")
    new_user = User(name=name)
    db.session.add(new_user)
    db.session.commit()
    return render_template("greet.html", name=name)


@app.route("/list")
def list_users():
    users = User.query.all()
    return render_template("list.html", users=users)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

