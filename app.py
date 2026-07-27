from flask import Flask , render_template , request
import sqlite3

app = Flask(__name__)

conn = sqlite3.connect("student.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
city TEXT,
age INTEGER
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS student_user(
username TEXT PRIMARY KEY,
password TEXT
)
""")

conn.commit()
conn.close()

@app.route("/")
def home():
    return render_template ("home.html")

@app.route("/signup", methods = ["GET", "POST"])
def signup():
    if request.method == "POST":
        
        username = request.form["username"]
        password = request.form["password"]

        conn   = sqlite3.connect("student.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM student_user WHERE username = ?",
        (username,)
        )
        user = cursor.fetchone()
        if user:
            print("error")
            return render_template ("signup.html")
        else:
            cursor.execute(
            "INSERT INTO student_user (username, password) VALUES (?,?)",
            (username, password)
            )

        conn.commit()
        conn.close()

        return render_template ("login.html")
    
    return render_template ("signup.html")

@app.route("/login", methods = ["GET","POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        conn   = sqlite3.connect("student.db")
        cursor = conn.cursor()

        cursor.execute(
        "SELECT * FROM student_user WHERE username = ? AND password = ?",
        (username, password)
        )

        user = cursor.fetchone()

        conn.close()

        if user :
            return render_template("dashboard.html")
        else:
            return render_template("login.html")

    return render_template ("login.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/register", methods = ["GET", "POST"])
def register():
    if request.method == "POST":

        name = request.form["name"]
        city = request.form["city"]
        age  = request.form["age"]
        
        conn   = sqlite3.connect("student.db")
        cursor = conn.cursor()

        cursor.execute(
        "INSERT INTO students (name, city, age) VALUES (?,?,?)",
        (name, city, age)
        )
        
        conn.commit()
        
        cursor.execute("SELECT * FROM students")
        students = cursor.fetchall()

        print(f"Registration Successful: {name}")

        print(students)

        conn.close()
        return render_template ("student.html", students = students)
    
    return render_template ("register.html")

@app.route("/search", methods = ["GET", "POST"])
def search():
    if request.method == "POST":
        
        id = request.form["id"]

        conn   = sqlite3.connect("student.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM students WHERE id = ?",
            (id,)
        )

        students = cursor.fetchall()
        conn.close()

        return render_template ("student.html", students = students)
        
    return render_template ("search.html")

@app.route("/update", methods = ["GET", "POST"])
def update():

    student = None

    if request.method == "POST":
        action = request.form["action"]

        if action == "search":
            id = request.form["id"]

            conn = sqlite3.connect("student.db")
            cursor = conn.cursor()

            cursor.execute(
                "SELECT * FROM students WHERE id = ?",
                (id,)
            )

            student = cursor.fetchone()

            conn.close()
            return render_template("update.html", student = student )
        
        elif action == "Update":
            
            id = request.form["id"]
            name = request.form["name"]
            city = request.form["city"]
            age = request.form["age"]

            conn = sqlite3.connect("student.db")
            cursor = conn.cursor()

            cursor.execute(
                """
                UPDATE students SET name=?, city=?, age=? WHERE id =?
                """,
                (name, city, age,id)
            )

            conn.commit()

            cursor.execute("SELECT * FROM students")

            students = cursor.fetchall()

            conn.close()
            return render_template("student.html", students = students )

    return render_template("update.html", student = student )

@app.route("/delete", methods = ["GET","POST"])
def delete():

    if request.method == "POST":

        id = request.form["id"]
    
        conn = sqlite3.connect("student.db")
        cursor = conn.cursor()
    
        cursor.execute(
        "DELETE FROM students WHERE id =?",
        (id,)
        )
        conn.commit()

        cursor.execute("SELECT * FROM students")
        Students = cursor.fetchall()

        conn.close()

        return render_template ("delete.html", Students = Students )
    
    return render_template ("delete.html")


if __name__ == "__main__":
    app.run(debug=True)