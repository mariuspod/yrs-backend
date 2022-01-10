
from flask import Flask, jsonify
from flask_cors import CORS

import yrs

app = Flask(__name__)
CORS(app)

@app.route("/", methods=['POST'])
def yrs_backend():
    return(jsonify(yrs.main()))
        
    

