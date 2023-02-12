from flask import Flask, render_template, request
from db_utils import Db_helper

application = Flask(__name__)

@application.route("/", methods =["GET", "POST"])
def main():
    if request.method == "POST":
        login_info = (request.form.get('login_username'), request.form.get('login_password'))
        login_info = list(filter(None, login_info))

        create_info = (request.form.get('create_username'), request.form.get('create_password'), request.form.get('create_email'))
        create_info = list(filter(None, create_info))
        dbh = Db_helper()
        if len(login_info) == 2:
            print("logged in: " , dbh.login(login_info[0], login_info[1]))
            pass
        elif len(create_info) == 3:
            dbh.create_user(create_info[0], create_info[1], create_info[2])
            print("creating account:")
            pass
        
        return render_template("login.html")
    return render_template("login.html")

@application.route("/home")
def home():
    return render_template("home.html")

@application.route("/projects")
def projects():
    return render_template("projects.html")

@application.route("/alltickets")
def all_tickets():
    return render_template("all_tickets.html")

@application.route("/newproject")
def add_project():
    return render_template("add_project.html")

@application.route("/project")
def cur_project():
    return render_template("project.html")

if __name__ == "__main__":
    application.run(debug=True, use_reloader=True, threaded=True)