from flask import Flask, request, redirect
import sqlite3

app = Flask(__name__)


# Create database and table
def init_db():
    conn = sqlite3.connect("placement.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            skills TEXT NOT NULL,
            status TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# Home page
@app.route("/")
def home():

    conn = sqlite3.connect("placement.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    conn.close()

    student_html = ""

    for student in students:
        student_html += f"""
        <div style="
            background:white;
            padding:15px;
            margin:15px 0;
            border-radius:10px;
            box-shadow:0 2px 5px #ccc;
        ">
            <h3>{student[1]}</h3>
            <p>Email: {student[2]}</p>
            <p>Skills: {student[3]}</p>
            <p>Status: <b>{student[4]}</b></p>
        </div>
        """

    return f"""
    <html>

    <head>
        <title>Student Placement Tracker</title>
    </head>

    <body style="
        font-family:Arial;
        background:#f4f6f8;
        padding:40px;
    ">

        <div style="
            max-width:700px;
            margin:auto;
        ">

            <h1>🎓 Student Placement Tracker</h1>

            <form action="/add" method="POST"
                style="
                background:white;
                padding:25px;
                border-radius:10px;
            ">

                <input
                    name="name"
                    placeholder="Student Name"
                    required
                    style="padding:10px;width:90%;margin:5px;"
                >

                <input
                    name="email"
                    type="email"
                    placeholder="Email"
                    required
                    style="padding:10px;width:90%;margin:5px;"
                >

                <input
                    name="skills"
                    placeholder="Skills (Python, Java, SQL)"
                    required
                    style="padding:10px;width:90%;margin:5px;"
                >

                <select
                    name="status"
                    style="padding:10px;width:94%;margin:5px;"
                >
                    <option>Looking for Placement</option>
                    <option>Applied</option>
                    <option>Interview</option>
                    <option>Selected</option>
                </select>

                <button
                    type="submit"
                    style="
                    padding:10px 20px;
                    margin:5px;
                    background:#222;
                    color:white;
                    border:none;
                    border-radius:5px;
                ">
                    Add Student
                </button>

            </form>

            <h2>Students</h2>

            {student_html}

        </div>

    </body>
    </html>
    """


# Add student
@app.route("/add", methods=["POST"])
def add_student():

    conn = sqlite3.connect("placement.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO students (name, email, skills, status)
        VALUES (?, ?, ?, ?)
    """, (
        request.form["name"],
        request.form["email"],
        request.form["skills"],
        request.form["status"]
    ))

    conn.commit()
    conn.close()

    return redirect("/")


# Start application
if __name__ == "__main__":
    init_db()
    app.run(debug=True)
