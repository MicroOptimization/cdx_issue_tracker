from flask import Flask, render_template

application = Flask(__name__)

@application.route("/")
def main():
    return render_template("login.html")

@application.route("/home")
def home():
    return render_template("home.html")

if __name__ == "__main__":
    application.run(debug=True, use_reloader=True, threaded=True)