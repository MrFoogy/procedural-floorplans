from flask import Flask, request
from flask_cors import CORS
from np_encoder import NpEncoder
import main
import json

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
    generations = json.loads(request.args.get("generations"))
    individuals = json.loads(request.args.get("individuals"))
    building_size = json.loads(request.args.get("building_size"))
    hof_size = json.loads(request.args.get("hof_size"))
    return json.dumps(main.run_ga(generations, individuals, building_size, hof_size, False), cls=NpEncoder)

if __name__ == "__main__":
    app.run()
