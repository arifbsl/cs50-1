import cs50
import csv

from flask import Flask, jsonify, redirect, render_template, request

# Configure application
app = Flask(__name__)

# Reload templates when they are changed
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.after_request
def after_request(response):
    """Disable caching"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# listens for / via method GET
@app.route("/", methods=["GET"])
def get_index():
    # redirects to /form
    return redirect("/form")

# listens for /form via method GET
@app.route("/form", methods=["GET"])
def get_form():
    # renders form template
    return render_template("form.html")

# listens for /form via method POST
@app.route("/form", methods=["POST"])
def post_form():
    if not request.form.get("name") or not request.form.get("pets") or not request.form.get("favorite"):
        return render_template("error.html", message="Please input all information")
    else:
        # writes input to csv file, and redirects to sheets
        file = open("survey.csv", "a")
        writer = csv.writer(file)
        writer.writerow((request.form.get("name"), request.form.get("pets"), request.form.get("favorite")))
        file.close()
        return redirect("/sheet")

# listens for /sheet via method GET
@app.route("/sheet", methods=["GET"])
def get_sheet():
    # opens csv file and inputs data into a table
    file = open("survey.csv", "r")
    file_info = csv.reader(file)
    final_info = list(file_info)
    file.close()
    
    return render_template("sheet.html", final_info=final_info, message="Survey Results")

