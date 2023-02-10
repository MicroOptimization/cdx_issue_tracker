from flask import Flask, render_template

application = Flask(__name__)

@application.route("/")
def main():
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