#import libraries
import requests
import json
import webbrowser
import warnings
import os
import time
import numpy as np
from csv import DictWriter
from bs4 import BeautifulSoup as soup
from datetime import datetime
import random

warnings.filterwarnings("ignore")
# set the url for the api
URL = 'https://iu-model.herokuapp.com/api/predict'
# mocking a sensor data stream in 5 seconds intervals
start_time = time.time()
seconds = 5
while True:

    current_time = time.time()
    elapsed_time= current_time-start_time

    if elapsed_time > seconds:

        # if 5 seconds have passed generate random sensor values
        sensor_data_t = round(random.uniform(20,120),2)
        sensor_data_h = round(random.uniform(0,100),2)
        sensor_data_v = round(random.uniform(10,130),2)

        req_data = json.dumps({"temperature":sensor_data_t,"humidity":sensor_data_h,"volume":sensor_data_v})

        # transform the data in the required json format

        # send the POST request to the api


        r = requests.post(url=URL,data=req_data)
        # read the html response and scrape the part that contains the prediction
        # create a dictionary and write the data and the temporary labels to a CSV file
        # Temporary in the sense that can be later updated with the real label after expert
        # inspection. Also the time is included to facilitate the inspection.
        html = r.text
        headersCSV = ['time','temperature','humidity','volume','labels']
        prediction_label = int(soup(html, 'html.parser').p1.text)
        data_dict = {'time':datetime.now().strftime("%d/%m/%Y %H:%M:%S"),'temperature':sensor_data_t,'humidity':sensor_data_h,'volume':sensor_data_v,'labels':prediction_label}



        with open('sensor_new_data.csv', 'a', newline='') as f_object:
            dictwriter_object = DictWriter(f_object, fieldnames=headersCSV)
            dictwriter_object.writerow(data_dict)
            f_object.close()
        path = os.getcwd()

        # opens the browser with the response html data and prediction
        # which is overwritten everytime there is a new response
        # 5 seconds
        f = open("home.html", "w")
        f.write(html)
        f.close()
        webbrowser.open('file://'+path+'/home.html')
        start_time = time.time()
