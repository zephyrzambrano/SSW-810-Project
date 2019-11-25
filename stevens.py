"""
Homework 12 by Zephyr Zambrano

Flas web server that dynamically displays instructor data in a table on a webpage.

"""


import sqlite3
from flask import Flask, render_template


app = Flask(__name__)


@app.route("/")
@app.route("/home")
def home():
    db_path = "/Users/Zephyr Zambrano/Documents/GitHub/SSW-810-Project/810_startup.db"
    db = sqlite3.connect(db_path)
    query = """select CWID, Name, Dept, Course, count(*) from instructors join grades on CWID = InstructorCWID
    group by CWID, Name, Dept, Course"""
    
    # convert query results into a list of dictionaries to pass to the template
    data = [{"cwid": cwid, "name": name, "department": department, "course": course, "students": students}
            for cwid, name, department, course, students in db.execute(query)]
    
    db.close() # close database connection
    
    return render_template("instructors.html", title="Stevens Repository", my_header="Stevens Repository", table_title="Courses and student counts", instructors=data)


app.run(debug=True) # only use for debugging; delete upon website deploy