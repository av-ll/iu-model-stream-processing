#importing libraries
import numpy as np
from flask import Flask,request,jsonify,render_template
import pickle
import json
import warnings
import os
import psycopg2
from datetime import datetime

warnings.filterwarnings("ignore")

#creating app name with Flask

app = Flask(__name__)
model = pickle.load(open('model.pkl','rb'))

# creating database

DATABASE_URL = os.environ['DATABASE_URL']

conn = psycopg2.connect(DATABASE_URL, sslmode='require')

cur = conn.cursor()

cur.execute("""
        CREATE TABLE IF NOT EXISTS new_sensor_data (
                item_id SERIAL PRIMARY KEY,
                time VARCHAR(30),
                temperature FLOAT8,
                humidity FLOAT8,
                volume FLOAT8
                
        );
        """)

#loading the model which was generated in pickle format

@app.route('/')
def home():
    return render_template('index.html')

# the app receives a json containing the data to be predicted
# displays the data received of each feature and the predicted
# probability, also returns an hidden label (0 or 1) which can then
# be scraped with beautiful soup or libraries like that
# and lastly also stores the value in a cloud postgre database in heroku
@app.route('/api/<predict>',methods=['POST'])
def predict(predict):
    received = request.get_json(predict)
    keys = list(received.keys())
    temp = keys[0]+': '+str(received[keys[0]])+'  °'
    humid = keys[1]+': '+str(received[keys[1]])+'%'
    vol = keys[2]+': '+str(received[keys[2]])+' db'
    received_list = [received[x] for x in received.keys()]
    final_features = np.array(received_list)
    prediction = model.predict_proba(final_features.reshape(1,-1))
    prediction = prediction.tolist()
    output = round(prediction[0][1]*100,2)
    prediction_label = int(model.predict(final_features.reshape(1,-1))[0])
    cur.execute("""
            INSERT INTO new_sensor_data VALUES (%s,%s,%s,%s);
            """,(str(datetime.now().strftime("%d/%m/%Y %H:%M:%S")),received[keys[0]],received[keys[1]],received[keys[2]]))
    
    return render_template('index.html',temperature=temp,humidity=humid,volume=vol,prediction_text='Probability of anomaly is {}%'.format(output),prediction = prediction_label)

# Main loop
if __name__ == '__main__':
    app.run(debug=True)
