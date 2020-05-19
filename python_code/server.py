from flask import Flask
from flask_cors import CORS
import main

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
    return main.run_ga(False)

if __name__ == "__main__":
    app.run()
