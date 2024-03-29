from flask import Flask, render_template, redirect, url_for ,send_file,request
from metadata.setup import init
from flask_cors import CORS, cross_origin
from utils.course_module import CourseManager,Course
from utils.index_generator import IndexGenerator
import os
import json

course_manager_master = CourseManager()
index_generator = IndexGenerator()



course_resumed = None


app = Flask(__name__) 
CORS(app, support_credentials=True)


# @app.route("/") 
# def home(): 
# 	return render_template("index.html") 


# @app.route("/default") 
# def default(): 
# 	return render_template("layout.html") 


# @app.route("/variable") 
# def var(): 
# 	user = "Geeksforgeeks"
# 	return render_template("variable_example.html", name=user) 

# @app.route("/if") 
# def ifelse(): 
# 	user = "Practice GeeksforGeeks"
# 	return render_template("if_example.html", name=user) 


# @app.route("/for") 
# def for_loop(): 
# 	list_of_courses = ['Java', 'Python', 'C++', 'MATLAB'] 
# 	return render_template("for_example.html", courses=list_of_courses) 


# @app.route("/choice/<pick>") 
# def choice(pick): 
# 	if pick == 'variable': 
# 		return redirect(url_for('var')) 
# 	if pick == 'if': 
# 		return redirect(url_for('ifelse')) 
# 	if pick == 'for': 
# 		return redirect(url_for('for_loop')) 

@app.route("/cdn/<path>")
def custom_static(path):
    path = str(path).replace(">",os.path.sep)    
    return send_file(path)


@app.route("/")
def home():
    return json.dumps(course_manager_master.listCourses())

@app.route("/homeData")
def homeData():
    return json.dumps(course_manager_master.listCourses())

@app.route("/add", methods=['GET', 'POST'])
def add():
    if request.method == 'GET':
        return render_template("add.html")
    else:
        body = json.loads(request.data)
        # add functionaliy
        course_manager_master.addCourse(Course(body.get("fullPath")))
        return "OK"
    
@app.route("/resume/<index>", methods=["GET"])
def resume(index):
    if request.method == "GET":
        return course_manager_master.courseList[int(index)].getJson()
    

@app.route("/update", methods=['POST','GET'])
def update():
    body = json.loads(request.data)
    result = course_manager_master.updatePlaytime(body)
    return str(result)




if __name__ == "__main__":
    init()
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run('0.0.0.0', port=5000) 
