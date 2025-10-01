# Goal
Render MCPを使ってPostgreSQLを作成し、Flaskアプリから接続できるようにする。  
ユーザーが入力した名前をDBに保存し、履歴を一覧表示できるWebアプリを構築してRenderにデプロイする。  

# Steps
1. Render MCPで `create_postgres` を実行して無料のPostgresインスタンスを作成する。  
2. Render MCPで `update_environment_variables` を使って、サービスに `DATABASE_URL` を設定する。  
3. 以下のファイルを作成する。  

## app.py
```python
import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

@app.before_first_request
def create_tables():
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
```

## requirements.txt
```
Flask==3.0.0
Flask-SQLAlchemy
psycopg2-binary
gunicorn
```

## Procfile
```
web: gunicorn app:app
```

## templates/index.html
```html
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>名前入力</title>
</head>
<body>
    <h1>名前を入力してください</h1>
    <form action="/greet" method="post">
        <input type="text" name="name" placeholder="名前を入力">
        <button type="submit">送信</button>
    </form>
    <p><a href="/list">登録済み一覧を見る</a></p>
</body>
</html>
```

## templates/greet.html
```html
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>挨拶</title>
</head>
<body>
    <h1>こんにちは、{{ name }}さん！</h1>
    <p><a href="/">戻る</a></p>
    <p><a href="/list">登録済み一覧を見る</a></p>
</body>
</html>
```

## templates/list.html
```html
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>登録一覧</title>
</head>
<body>
    <h1>登録されたユーザー一覧</h1>
    <ul>
        {% for user in users %}
        <li>{{ user.name }}</li>
        {% endfor %}
    </ul>
    <p><a href="/">トップに戻る</a></p>
</body>
</html>
```

# Git Commands
```bash
git init
git add .
git commit -m "Flask app with Postgres"
git branch -M main
git remote add origin git@github.com:<USERNAME>/<REPO>.git
git push -u origin main
```

# Expected Result
- `/` でフォーム入力  
- `/greet` で入力内容をDBに保存して挨拶表示  
- `/list` で登録済みユーザー一覧を表示  

