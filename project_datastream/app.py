#importing libraries
import numpy as np
from flask import Flask,request,jsonify,render_template
import pickle
import json
import warnings

warnings.filterwarnings("ignore")

#creating app with Flask

app = Flask(__name__)
model = pickle.load(open('model.pkl','rb'))

#loading the model which was generated in pickle format

@app.route('/')
def home():
    return render_template('index.html')

# the app receives a json containing the data to be predicted
# displays the data received of each feature and the predicted
# probability, also returns an hidden label (0 or 1) which can then
# be scraped with beautiful soup or libraries like that
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
    return render_template('index.html',temperature=temp,humidity=humid,volume=vol,prediction_text='Probability of anomaly is {}%'.format(output),prediction = prediction_label)

# Main loop
if __name__ == '__main__':
    app.run(debug=True)
