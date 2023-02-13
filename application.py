from flask import Flask, render_template, request, session, redirect, g
from db_utils import Db_helper
import secrets

application = Flask(__name__)
application.secret_key = secrets.token_urlsafe(16)

@application.context_processor
def inject_user():
    return dict(username=session.get("username"))
        
@application.route("/", methods =["GET", "POST"])
def main():
    if request.method == "POST":
        login_info = (request.form.get('login_username'), request.form.get('login_password'))
        login_info = list(filter(None, login_info))

        create_info = (request.form.get('create_username'), request.form.get('create_password'), request.form.get('create_email'))
        create_info = list(filter(None, create_info))
        
        dbh = Db_helper()     
        if len(login_info) == 2: #we've identified that we're TRYING to log in
            res = dbh.login(login_info[0], login_info[1])
            print(type(res))
            if res[0]: #if login succeeded
                print("log in success")
                application.secret_key = secrets.token_urlsafe(16) #so this resets the session
                #res[1] is a dict of all the columns from the user row we got when we did dbh.login

                session["logged_in"] = True
                session["username"] = res[1]["username"]
                session["user_id"] = res[1]["user_id"]

                return redirect("/home") #lets you into the home page
            else: #incorrect password or username.
                print("login failed")
                return redirect("/")
        elif len(create_info) == 3: #we've identified that we're TRYING to make a new account
            if dbh.create_user(create_info[0], create_info[1], create_info[2]): #dbh.create_user will return true if the account was made successfully
                print("acc created successfully!")
            else:
                print("username or email taken!")
            pass
        return render_template("login.html")
    return render_template("login.html")

@application.route("/logout")
def logout():
    session.clear()
    application.secret_key = secrets.token_urlsafe(16) #so this resets the session
    return redirect("/")

@application.route("/home", methods= ["POST", "GET"])
def home():
    return render_template("home.html", username=session["username"])

@application.route("/alltickets")
def all_tickets():
    return render_template("all_tickets.html")

@application.route("/newproject", methods=["GET", "POST"])
def add_project():
    if request.method == "POST":
        project_details = (request.form.get("pinput"), request.form.get("kinput"), request.form.get("dinput"))
        dbh = Db_helper()
        print(session)
        print("sid: " , session["user_id"])
        res = dbh.create_project(project_details, session["user_id"])
        pass
    return render_template("add_project.html")

@application.route("/projects")
def projects():
    return render_template("projects.html")

@application.route("/project")
def cur_project():
    return render_template("project.html")

if __name__ == "__main__":
    application.run(debug=True, use_reloader=True, threaded=True)