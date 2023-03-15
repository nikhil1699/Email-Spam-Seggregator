from flask import Flask, request, render_template

import spam_detector
from functions import *
import imaplib

app = Flask(__name__)

body_rows = []
subject_rows = []

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def generate_file():
    global subject_rows
    global body_rows
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
    subject_rows = subjects.split("\n####################")

    return render_template('index.html', rows=rows, body_rows=body_rows, subject_rows=subject_rows)


@app.route('/is-spam/', methods=['POST'])
def is_spam():
    subject = request.form['subject']  # get the subject for them email we will predict based on button clicked
    ind = subject_rows.index(subject.strip())
    body = body_rows[ind]
    result = spam_detector.predict_spam(subject=subject, body=body)
    if result:
        return "This looks like a SPAM"
    else:
        return "This looks like a HAM"
