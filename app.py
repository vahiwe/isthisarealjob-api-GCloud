from flask import Flask, render_template, url_for, request, jsonify, redirect
import requests
import pandas
from bs4 import BeautifulSoup
from textblob import TextBlob
import matplotlib.pyplot as plt
import urllib
import nltk, os
nltk_dir = os.path.join(os.getcwd(), 'nltk_data')
nltk.data.path.append(nltk_dir)
import spacy
import queue
from threading import Thread
# import en_core_web_sm
from PIL import Image
from gingerit.gingerit import GingerIt
import googlemaps
from time import time
from grammer import *
from address import *
from nairaland import *
from confidence import *
# from cac_check import *

# nltk.download("stopwords")
# nltk.download("punkt")
from nltk.corpus import stopwords

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    """
    GET Request
    """
    # Give message to user
    return redirect("https://documenter.getpostman.com/view/9310664/SW132eE3?version=latest")


@app.route('/', methods=['POST'])
def analyze():
    """
    POST Request
    """
    start_time = time()
    data = request.get_json(force=True)
    try:
        searchTerm = data['company']
        addressTerm = data['address']
        inviteTerm = data['invite']
        # data = [data]
    except KeyError:
        titl = "You have a KeyError. Please check your JSON input"
        return jsonify(errors=titl)

    jobres = []
    que = queue.Queue()
    threads_list = list()

    t = Thread(target=lambda q, arg1: q.put(nairasearch(arg1)), args=(que, searchTerm))
    t.start()
    threads_list.append(t)

    # t2 = Thread(target=lambda q, arg1: q.put(scraper(arg1)), args=(que, searchTerm))
    # t2.start()
    # threads_list.append(t2)

    t3 = Thread(target=lambda q, arg1: q.put(verify_address(arg1)), args=(que, addressTerm))
    t3.start()
    threads_list.append(t3)

    # Join all the threads
    for t in threads_list:
        t.join()

    # Check thread's return value
    while not que.empty():
        result = que.get()
        jobres.append(result)


    for i in range(len(jobres)):
        # if isinstance(jobres[i], pandas.core.frame.DataFrame):
        #     dg = jobres[i]
        if isinstance(jobres[i], int) or isinstance(jobres[i], float):
            negative = jobres[i]
        if isinstance(jobres[i], str):
            addr = jobres[i]


    # if dg.empty:
    #     cac = True
    # else:
    #     cac = False


    if addr == "The Company address is valid":
        cont = "This address looks legit"
        auth = True
    else:
        cont = "This address might be bogus"
        auth = False


    inv = check(inviteTerm)
    correction = inv
    if inv == 0:
        contt = "There are no errors in this invitation"
    else:
        contt = "You have errors in this invitation"


    report = confidence_interval(correction, auth, negative)
    print('Time to solve: ', time() - start_time)
    return jsonify(confidence=report)

@app.route('/form', methods=['POST'])
def analyze_form():
    """
    POST Request
    """
    try:
        searchTerm = request.form['company']
        addressTerm = request.form['address']
        inviteTerm = request.form['invite']
        # data = [data]
    except KeyError:
        titl = "You have a KeyError. Please check your Form input"
        return jsonify(errors=titl)


    jobres = []
    que = queue.Queue()
    threads_list = list()

    t = Thread(target=lambda q, arg1: q.put(nairasearch(arg1)), args=(que, searchTerm))
    t.start()
    threads_list.append(t)

    # t2 = Thread(target=lambda q, arg1: q.put(scraper(arg1)), args=(que, searchTerm))
    # t2.start()
    # threads_list.append(t2)

    t3 = Thread(target=lambda q, arg1: q.put(verify_address(arg1)), args=(que, addressTerm))
    t3.start()
    threads_list.append(t3)

    # Join all the threads
    for t in threads_list:
        t.join()

    # Check thread's return value
    while not que.empty():
        result = que.get()
        jobres.append(result)


    for i in range(len(jobres)):
        # if isinstance(jobres[i], pandas.core.frame.DataFrame):
        #     dg = jobres[i]
        if isinstance(jobres[i], int) or isinstance(jobres[i], float):
            negative = jobres[i]
        if isinstance(jobres[i], str):
            addr = jobres[i]


    # if dg.empty:
    #     cac = True
    # else:
    #     cac = False


    if addr == "The Company address is valid":
        cont = "This address looks legit"
        auth = True
    else:
        cont = "This address might be bogus"
        auth = False


    inv = check(inviteTerm)
    correction = inv
    if inv == 0:
        contt = "There are no errors in this invitation"
    else:
        contt = "You have errors in this invitation"


    report = confidence_interval(correction, auth, negative)
    # print('Time to solve: ', time() - start_time)
    return jsonify(confidence=report)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)