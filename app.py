from flask import Flask, request, render_template
from functions import *
import imaplib

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def generate_file():
    user = request.form['user']
    password = request.form["password"]
    sender_email_id = request.form['sender_email_id']
    collect_emails(user, password, sender_email_id)
    # Read file contents and display on web page
    string_boxes = []
    with open(f"{sender_email_id}-emails", 'r') as f:
        contents = f.read()
    rows = contents.split("####################")

    with open(f"{sender_email_id}-bodies", 'r') as f:
        bodies = f.read()
    body_rows = bodies.split("####################")

    with open(f"{sender_email_id}-subjects", 'r') as f:
        subjects = f.read()
    subject_rows = subjects.split("####################")

    return render_template('index.html', rows=rows, body_rows=body_rows, subject_rows=subject_rows)
