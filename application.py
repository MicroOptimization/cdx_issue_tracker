from flask import Flask, render_template, request, session, redirect
from db_utils import Db_helper
import secrets

application = Flask(__name__)
application.secret_key = secrets.token_urlsafe(16)

@application.route("/", methods =["GET", "POST"])
def main():
    if request.method == "POST":
        login_info = (request.form.get('login_username'), request.form.get('login_password'))
        login_info = list(filter(None, login_info))

        create_info = (request.form.get('create_username'), request.form.get('create_password'), request.form.get('create_email'))
        create_info = list(filter(None, create_info))
        
        dbh = Db_helper()     
        if len(login_info) == 2:
            res = dbh.login(login_info[0], login_info[1])
            print(type(res))
            if res[0]: #if login succeeded
                print("log in success")
                application.secret_key = secrets.token_urlsafe(16) #so this resets the session
                #res[1] is a dict of all the columns from the user row we got when we did dbh.login

                session["logged_in"] = True
                session["username"] = res[1]["username"]
                session["user_id"] = res[1]["user_id"]
                print(session["username"], session["user_id"])
            else:
                print("login failed")
                return redirect("/")
        elif len(create_info) == 3:
            if dbh.create_user(create_info[0], create_info[1], create_info[2]):
                print("acc created successfully!")
            else:
                print("username or email taken!")
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