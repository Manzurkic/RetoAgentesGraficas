from flask import Flask, request, jsonify
import json
import logging
import os
import atexit
from ModeloTrafico import TraficModel

app = Flask(__name__, static_url_path='')
model = TraficModel(24, 24, 24)


def positionsToJSON(ps):
    posDict = []
    for p in ps:
        pos = {
            "x": p[0],
            "z": p[1],
            "y": p[2],
        }
        posDict.append(pos)
    return json.dumps(posDict)


port = int(os.getenv('PORT', 8585))


@app.route('/')
def root():
    return jsonify([{"message": "Hello World from IBM Cloud"}])


@app.route('/multiagentes')
def multiagentes():
    positions = model.step()
    return positionsToJSON(positions)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)
