# Importing libraries
import imaplib, email
import pprint
imap_url = 'imap.gmail.com'


# Possible inputs
# (\HasNoChildren) "/" "College Folder"
# (\HasNoChildren) "/" "INBOX"
# (\HasNoChildren) "/" "Notes"
# (\HasChildren \Noselect) "/" "[Gmail]"
# (\All \HasNoChildren) "/" "[Gmail]/All Mail"
# (\Drafts \HasNoChildren) "/" "[Gmail]/Drafts"
# (\HasNoChildren \Important) "/" "[Gmail]/Important"
# (\HasNoChildren \Sent) "/" "[Gmail]/Sent Mail"
# (\HasNoChildren \Junk) "/" "[Gmail]/Spam"
# (\Flagged \HasNoChildren) "/" "[Gmail]/Starred"
# (\HasNoChildren \Trash) "/" "[Gmail]/Trash
# """

# Function to get email content part i.e its body part
def get_body(msg):
    if msg.is_multipart():
        return get_body(msg.get_payload(0))
    else:
        return msg.get_payload(None, True)


# Function to search for a key value pair
def search(key, value, con):
    result, data = con.search(None, key, '"{}"'.format(value))
    return data


# Function to get the list of emails under this label
def get_emails(con, result_bytes):
    msgs = []  # all the email data are pushed inside an array
    for num in result_bytes[0].split():
        typ, data = con.fetch(num, '(RFC822)')
        msgs.append(data)

    return msgs


def collect_emails(user, password, sender_email_id):
    # this is done to make SSL connection with GMAIL
    con = imaplib.IMAP4_SSL(imap_url)
    # logging the user in
    con.login(user, password)

    # calling function to check for email under this label
    code, mailboxes = con.list()
    con.select('"[Gmail]/All Mail"')
    # fetching emails from this user
    msgs = get_emails(con, search('FROM', sender_email_id, con))
    if len(msgs) == 0:
        con.select('"[Gmail]/Spam"')
        msgs = get_emails(con, search('FROM', sender_email_id, con))

    # print(len(msgs))
    mails = []
    for msg in msgs[::-1]:
        for sent in msg:
            if type(sent) is tuple:
                # encoding set as utf-8
                content = str(sent[1], 'utf-8')
                data = str(content)

                # Handling errors related to unicodenecode
                try:
                    indexstart = data.find("ltr")
                    data2 = data[indexstart + 5: len(data)]
                    indexend = data2.find("</div>")
                    # appending the required content which we need
                    # to extract from our email i.e our body
                    mails.append(data2[0: indexend])
                except UnicodeEncodeError as e:
                    pass

    # print("Printing mails")
    # print(len(mails))
    bodies = []
    subjects = []
    for mail in mails:
        from email.parser import Parser
        parser = Parser()
        email = parser.parsestr(mail)
        #pprint.pprint(email)
        #subjects.append(str(email.get('Subject')))
        subjects.append(str(email.get('Subject')))
        if email.is_multipart():
            for part in email.get_payload():
                bodies.append(str(part.get_payload()))
        else:
            bodies.append(str(email.get_payload()))
        #bodies.append(email.get_payload())
    print(len(subjects))
    print(len(bodies))

    with open(f"{sender_email_id}-emails", "w") as f:
        for item in mails:
            print(type(item))
            f.write(item + "\n")
            f.write(f"####################")

    with open(f"{sender_email_id}-bodies", "w") as f:
        for body in bodies:
            print(type(body))
            f.write(body+ "\n")
            f.write(f"####################")

    with open(f"{sender_email_id}-subjects", "w") as f:
        for subject in subjects:
            f.write(subject + "\n")
            f.write(f"####################")
