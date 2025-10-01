import os
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

# Prefer DATABASE_URL provided by Render Postgres; fallback for local dev
database_url = os.environ.get("DATABASE_URL", "sqlite:///local.db")
app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)


def ensure_tables():
    try:
        db.create_all()
    except Exception:
        # 起動直後のDB未準備や一時的な接続失敗時でもアプリを起動させる
        pass


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/greet", methods=["POST"])
def greet():
    name = request.form.get("name", "名無し")
    ensure_tables()
    new_user = User(name=name)
    db.session.add(new_user)
    db.session.commit()
    return render_template("greet.html", name=name)


@app.route("/list")
def list_users():
    ensure_tables()
    users = User.query.all()
    return render_template("list.html", users=users)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
