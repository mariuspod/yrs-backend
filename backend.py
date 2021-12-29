from flask import Flask
from config import connect_db
db = connect_db()
from pony.orm import db_session

app = Flask(__name__)

@app.route("/")
def hello_yrs_backend():
    with db_session:
      result = db.select('NOW()')
      return f"<p>Hello, yrs-backend!</p><p>it's {result[0]}</p>"

