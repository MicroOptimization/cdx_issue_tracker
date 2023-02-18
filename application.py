from flask import Flask, render_template, request, session, redirect, g, jsonify
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
    dbh = Db_helper()
    tickets = dbh.get_user_tickets(session["user_id"])
    return render_template("all_tickets.html", tickets=tickets)

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
        cols = dbh.get_cols(pid)
        tickets = {}
        for col in cols:
            cur_col_tickets = dbh.get_tickets_from_col(col["col_id"])
            if len(cur_col_tickets) != 0:
                tickets[col["col_id"]] = cur_col_tickets

        return render_template("project.html", project=project_info[0], cols=cols, tickets=tickets)
    return render_template("project.html")

@application.route("/deleteticket/<int:pid>", methods= ["POST", "GET"])
def delete_ticket(pid):
    if request.form['delete_btn'] == "delete":
        delete_me_id = request.form.get("ticket_id")
        dbh = Db_helper()
        dbh.remove_ticket(delete_me_id)
    
    return redirect("/project/" + str(pid))



@application.route("/newticket/<int:pid>/<int:cid>", methods=["POST", "GET"])
def add_ticket(pid, cid):
    if request.method == "POST":
        dbh = Db_helper()
        project_name = dbh.get_project_title_from_id(pid)
        ticket_info = {
            "title" : request.form.get("ninput"), 
            "description" : request.form.get("dinput"),
            "project_title" : project_name,
            "col_id": cid
        }
        dbh.create_ticket(pid, ticket_info)
        cur_project_url = "/project/" + str(pid) #redirects you to the project that you added a ticket to after you submit your ticket 
        return redirect(cur_project_url) 
    return render_template("add_ticket.html")

@application.route("/ticket/<int:tid>")
def ticket(tid):
    dbh = Db_helper()
    tinfo = dbh.get_ticket_info_by_id(tid)
    return render_template("ticket.html", ticket_info = tinfo)

@application.route("/createcol/<int:pid>", methods=["POST", "GET"])
def add_col(pid):
    if request.form['create_col_btn'] == "create":
        dbh = Db_helper()
        dbh.add_col(pid, request.form.get("col_name"))
    return redirect("/project/" + str(pid))

@application.route("/deletecol/<int:pid>/<int:cid>", methods=["POST", "GET"])
def delete_col(pid, cid):
    dbh = Db_helper()
    dbh.delete_col(cid)
    return redirect("/project/" + str(pid)) 



@application.route("/manageproject/<int:pid>")
def manage_project(pid):
    dbh = Db_helper()
    tickets = dbh.get_project_tickets(pid)
    users = dbh.get_project_users(pid)

    return render_template("manage_project.html", tickets=tickets, users=users, pid=pid)

@application.route("/adduser/<int:pid>", methods=["POST", "GET"])
def add_user(pid):
    dbh = Db_helper()
    email = request.form.get("email")

    uid = dbh.get_uid_by_email(email)
    dbh.add_user_to_project(uid, pid)

    return redirect("/manageproject/" + str(pid))

@application.route("/removeuser/<int:pid>/<int:uid>", methods=["POST", "GET"])
def remove_user(pid, uid):
    dbh = Db_helper()
    dbh.remove_user_from_project(uid, pid)
    return redirect("/manageproject/" + str(pid))

@application.route("/assignticket/<int:tid>/<int:pid>", methods=["POST", "GET"])
def assign_ticket(tid, pid):
    user_id = int(request.form.get("ticket_info_" + str(tid)))
    if user_id != "undefined": #if user_id is undefined, that means a user was not selected before button press.
        dbh = Db_helper()
        dbh.assign_ticket_to_user(user_id, tid)
    return redirect("/manageproject/" + str(pid))

@application.route('/updatedesc', methods=['POST', 'GET'])
def update_desc():
    if request.method == "POST":
        desc_data = request.get_json()
        new_text = desc_data["new_text"]
        pid = desc_data["project_id"]

        print(new_text, pid)
        dbh = Db_helper()
        dbh.edit_project_desc(pid, new_text)

    results = {'updated': 'true'}
    return jsonify(results)

@application.route('/updatetitle', methods=['POST', 'GET'])
def update_title():
    if request.method == "POST":
        title_data = request.get_json()
        new_title = title_data["new_title"]
        pid = title_data["project_id"]

        dbh = Db_helper()
        dbh.edit_project_title(pid, new_title)

    results = {'updated': 'true'}
    return jsonify(results)

@application.route('/updateticketdesc', methods=['POST', 'GET'])
def update_ticket_desc():
    if request.method == "POST":
        desc_data = request.get_json()
        new_desc = desc_data["new_desc"]
        tid = desc_data["ticket_id"]
        dbh = Db_helper()
        dbh.edit_ticket_desc(tid, new_desc)
    results = {'updated': 'true'}
    return jsonify(results)

@application.route('/updatetickettitle', methods=['POST', 'GET'])
def update_ticket_title():
    if request.method == "POST":
        title_data = request.get_json()
        new_title = title_data["new_title"]
        tid = title_data["ticket_id"]
        dbh = Db_helper()
        dbh.edit_ticket_title(tid, new_title)
    results = {'updated': 'true'}
    return jsonify(results)

if __name__ == "__main__":
    application.run(debug=True, use_reloader=True, threaded=True)