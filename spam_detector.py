import pickle
import pandas as pd
import re
import string
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from zipfile import ZipFile
pd.options.mode.chained_assignment = None  # default='warn' suppress the warning for new_df=features.iloc[0:0]

NEWLINE = '\n'
CLEAN = re.compile(r'<[^>]+>')
SW_NLTK = set(stopwords.words('english'))

with ZipFile("final_pj_model.zip", 'r') as zip:
    zip.extractall()

scaler = pickle.load(open('final_pj_scaler', 'rb'))
model = pickle.load(open('final_pj_model', 'rb'))
features = pd.read_pickle("final_pj_features")


def preprocess_body(body):
    # remove extra white spaces
    body = " ".join(body.split())

    # remove numbers
    body = ''.join([i for i in body if not i.isdigit()])

    # remove urls
    body = re.sub(r'http\S+', '', body)

    # remove all HTML tags
    body = re.sub(CLEAN, '', body)

    # to lowercase
    body = body.lower()

    # apply stop words removal and stemming
    processed_body = ""
    porter = PorterStemmer()
    word_tokens = word_tokenize(body)
    for word in word_tokens:
        if word not in SW_NLTK:
            stemmed = porter.stem(word.lower())
            processed_body += stemmed + " "

    # remove punctuation
    processed_body = processed_body.translate(str.maketrans('', '', string.punctuation))
    return processed_body


def word_count(str):
    counts = dict()
    words = str.split()

    for word in words:
        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1

    return counts


# returns true if email is spam, false otherwise
def predict_spam(subject, body):
    subject = preprocess_body(subject)
    body = preprocess_body(body)
    subject_body = body + subject

    # create data frame that contains the features
    new_df = features[0:0]

    # add the email features to the new_df
    row = []
    word_c_email = word_count(subject_body)
    for c in new_df.columns:
        if c in word_c_email:
            row.append(word_c_email[c])
        else:
            row.append(0.0)
    new_df.loc[len(new_df.index)] = row

    # scale and predict
    new_df = scaler.transform(new_df)
    predict_values_test = model.predict(new_df)
    if predict_values_test[0] == 0:
        return False
    else:
        return True

