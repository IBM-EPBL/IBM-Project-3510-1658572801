from flask import Flask, render_template,request
from feature import FeatureExtraction
import numpy as np
import joblib

app = Flask(__name__)

@app.route('/',methods=['GET'])
def hello():
    return render_template('index.html')

@app.route("/", methods=["POST"])
def index(): 
        url = request.form['url']
        obj = FeatureExtraction(url)
        x = np.array(obj.getFeaturesList()).reshape(1,30) 
        gbc = joblib.load('model.pkl')
        y_pred =gbc.predict(x)[0]
        #1 is safe       
        #-1 is unsafe
        y_pro_phishing = gbc.predict_proba(x)[0,0]
        y_pro_non_phishing = gbc.predict_proba(x)[0,1]
        if(y_pred == 0 ):
            url = "https://"+url 
        pred = "It is {0:.2f} % safe to go ".format(y_pro_phishing*100)
        return render_template('index.html',xx =round(y_pro_non_phishing,2),url=url )
if __name__ =='__main__':
    app.run(port=5500,debug=True)
