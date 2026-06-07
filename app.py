from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "remuse_secret_key"


def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT UNIQUE,
            password TEXT,
            exam TEXT
        )
    """)

    conn.commit()
    conn.close()


@app.route("/")
def home():
    return redirect("/login")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        exam = request.form["exam"]

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        try:
            cursor.execute(
                "INSERT INTO users (name, email, password, exam) VALUES (?, ?, ?, ?)",
                (name, email, password, exam)
            )
            conn.commit()
            conn.close()
            return redirect("/login")
        except:
            conn.close()
            return "Email already registered"

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE email=? AND password=?",
            (email, password)
        )

        user = cursor.fetchone()
        conn.close()

        if user:
            session["name"] = user[1]
            session["email"] = user[2]
            session["exam"] = user[4]
            return redirect("/dashboard")
        else:
            return "Invalid email or password"

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    if "email" not in session:
        return redirect("/login")

    return render_template("dashboard.html")


@app.route("/mock-tests")
def mock_tests():
    if "email" not in session:
        return redirect("/login")

    return render_template("mocktest.html")


@app.route("/submit-test", methods=["POST"])
def submit_test():
    if "email" not in session:
        return redirect("/login")

    score = 0

    if request.form.get("q1") == "Delhi":
        score += 1

    if request.form.get("q2") == "50":
        score += 1

    if request.form.get("q3") == "Dr B R Ambedkar":
        score += 1

    return render_template("result.html", score=score)


@app.route("/study-materials")
def study_materials():
    if "email" not in session:
        return redirect("/login")

    return render_template("material.html")


@app.route("/current-affairs")
def current_affairs():
    if "email" not in session:
        return redirect("/login")

    return render_template("current_affairs.html")


@app.route("/profile")
def profile():
    if "email" not in session:
        return redirect("/login")

    return render_template(
        "profile.html",
        name=session.get("name"),
        email=session.get("email"),
        exam=session.get("exam")
    )


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


if __name__ == "__main__":
    init_db()
    app.run(debug=True)