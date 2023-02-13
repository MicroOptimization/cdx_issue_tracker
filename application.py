from flask import Flask, render_template, request, session, redirect, g
from db_utils import Db_helper
import secrets

application = Flask(__name__)
application.secret_key = secrets.token_urlsafe(16)

@application.context_processor
def inject_user():
    return dict(username=session.get("username"))
        
@application.route("/", methods =["GET", "POST"]) #the login page
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

@application.route("/home")
def home():
    return render_template("home.html")

@application.route("/alltickets")
def all_tickets():
    return render_template("all_tickets.html")

@application.route("/newproject", methods=["GET", "POST"])
def add_project():
    if request.method == "POST":
        project_details = (request.form.get("pinput"), request.form.get("kinput"), request.form.get("dinput"))
        dbh = Db_helper()
        res = dbh.create_project(project_details, session["user_id"])
        #maybe return a render template for the project page that you just made
        pass
    return render_template("add_project.html")

@application.route("/projects")
def projects():
    dbh = Db_helper()
    pids = dbh.get_pids(session["user_id"])
    pinfo = dbh.get_project_info(pids)

    #let jinja use variables in the parameters of render_template for example we created the variable 
    #"project_info" that'll be used later in our html by jinja
    return render_template("projects.html", project_info=pinfo)

@application.route("/project/<int:pid>", methods=["POST", "GET"])
def cur_project(pid):
    
    if request.method == "GET":
        dbh = Db_helper()
        project_info = dbh.get_project_info([pid])

        return render_template("project.html", project=project_info[0])
    return render_template("project.html")

@application.route("/newticket/<int:pid>", methods=["POST", "GET"])
def add_ticket(pid):
    if request.method == "POST":
        ticket_info = {
            "title" : request.form.get("ninput"), 
            "description" : request.form.get("dinput")
        }
        #print(ticket_info)
        dbh = Db_helper()
        dbh.create_ticket(pid, ticket_info)
        pass
    return render_template("add_ticket.html")


if __name__ == "__main__":
    application.run(debug=True, use_reloader=True, threaded=True)