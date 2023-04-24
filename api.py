from flask import Flask, jsonify, send_from_directory, request
from flask_cors import CORS
import os

from pass_area import get_pass_area_data
from danger_pass import get_danger_pass
from heatmap import get_heatmap
from teamheatmap import get_teamheatmap


app = Flask(__name__)
CORS(app)


@app.route('/files')
def list_files():
    folder_path = "./StatsBomb/Data/"
    files = [f for f in os.listdir(folder_path) if os.path.isfile(
        os.path.join(folder_path, f)) and f.endswith("events.json")]
    return jsonify(files)

@app.route('/files_loc')
def list_files_loc():
    folder_path = "./Data/"
    files = [f for f in os.listdir(folder_path) if os.path.isfile(
        os.path.join(folder_path, f)) and f.endswith("meta.json")]
    return jsonify(files)

@app.route('/pass/<file>')
def pass_area(file):
    if os.path.isfile("./reports/" + file+"_pass_area.png"):
        output = "./reports/" + file+"_pass_area.png"
    else:
        output = get_pass_area_data(file,   "./reports/" + file+"_pass_area.png")
    return (output)

@app.route('/danger_pass/<file>')
def danger_pass(file):
    if os.path.isfile("./reports/" + file+"_danger_pass_2.png"):
        output = ["./reports/" + file+"_danger_pass_1.png","reports/" + file+"_danger_pass_2.png"]
    else:
        output = get_danger_pass(file,   "./reports/" + file+"_danger_pass_1.png", "./reports/" + file+"_danger_pass_2.png")

    return (output)

@app.route('/teamheatmap/<file>')
def teamheatmap(file):
    print(file)
    if os.path.isfile("./reports/" + file+"_team1heatmap.png"):
        output = ["./reports/" + file+"_team1heatmap.png","./reports/" + file+"_team2heatmap.png"]
    else:
        output = get_teamheatmap(file,   "./reports/"+file+"_team1heatmap.png", "./reports/"+file+"_team2heatmap.png")
    rep = {
        'team1': output[0],
        'team2': output[1]
    }
    return jsonify(rep)


@app.route('/heatmap/',methods=['GET'])
def heatmap():
    file=request.args['file']
    number=request.args['number']
    team=request.args['team']
    if os.path.isfile("reports/" + file+"_"+team+"_"+number+"_heatmap.png"):
        output = "reports/" + file+"_"+team+"_"+number+"_heatmap.png"
    else:
        output = get_heatmap(file,   "reports/" + file+"_"+team+"_"+number+"_heatmap.png",team,number)
    return jsonify(output)


@app.route('/reports/<path:path>')
def send_report(path):
    return send_from_directory('reports', path)

@app.route('/all/<file>')
def all(file):
    rep={
        'out0' : pass_area(file),
        'out1' : danger_pass(file)[0],
        'out2' : danger_pass(file)[1]
    }

    return(jsonify(rep))


if __name__ == '__main__':
    app.run()