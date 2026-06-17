import json
from flask import request, Flask, jsonify, make_response
import os
import random
import datastructure
import idgenerator

app = Flask(__name__)

def load_environment():

    base_dir = os.path.dirname(os.path.abspath(__file__))
    env_path = os.path.join(base_dir, 'dev_env.json')

    try:
        env_var = os.environ['WORKING_ENV']
    except:
        env_var = 'dev_env.json'

    with open(env_path) as f:
        env_values = json.loads(f.read())

    return env_values


@app.route('/', methods=['GET'])
def index():
    """Simple method to get some information about the software"""
    return json.dumps({'name': 'David',
                       'mail': 'david.herzig@fhnw.ch',
                       'System': 'Digital Biomarker Course Project',
                       'Server Component': 'v1_0_0',
                       'Date': '15-Apr-2026'})


@app.route('/experiment', methods=['POST', 'GET'])
def experiment_action():
    ds = datastructure.DataStorage()
    if request.method == 'POST':
        body = request.get_json()
        name = body['name']
        experiment_obj = datastructure.Experiment(name)
        ds.add_experiment(experiment_obj)
        return jsonify(experiment_obj.__dict__)
    if request.method == 'GET':
        id = request.args.get('id')
        result = ds.get_experiment(id)
        if result == None:
            return make_response(jsonify('experiment not found'), 404)
        else:
            return make_response(jsonify(result.__dict__), 200)


@app.route('/patient', methods=['POST', 'GET'])
def patient_action():
    ds = datastructure.DataStorage()
    if request.method == 'POST':
        body = request.get_json()
        name = body['name']
        patient_obj = datastructure.Patient(name)
        ds.add_patient(patient_obj)
        return jsonify(patient_obj.__dict__)
    if request.method == 'GET':
        id = request.args.get('id')
        result = ds.get_patient(id)
        if result == None:
            return make_response(jsonify('patient not found'), 404)
        else:
            return make_response(jsonify(result.__dict__), 200)


@app.route('/patients', methods=['GET'])
def patients_action():
    ds = datastructure.DataStorage()
    return json.dumps(ds.patients, cls=datastructure.PatientEncoder)


@app.route('/experiments', methods=['GET'])
def experiments_action():
    ds = datastructure.DataStorage()
    return json.dumps(ds.experiments, cls=datastructure.ExperimentEncoder)


@app.route('/store', methods=['POST'])
def store_data():
    ds = datastructure.DataStorage()
    ds.store_data()
    return make_response(jsonify("True"), 200)

#@app.route('/upload', methods=['POST'])
#@app.route('/data', methods=['POST'])
#def upload_data():
    ds = datastructure.DataStorage()
    if request.method == 'POST':
        body = request.get_json()
        print(body)
        patient_id = body['patientId']
        experiment_id = body['experimentId']
        data = body
        data_obj = datastructure.DataPoint(patient_id, experiment_id, data)
        ds.add_data(data_obj)
        return make_response('', 200)
    
@app.route('/data', methods=['POST'])
def upload_data():
    ds = datastructure.DataStorage()
    if request.method == 'POST':
        body = request.get_json()
        patient_id = body['patientId']
        experiment_id = body['experimentId']

        data_obj = datastructure.DataPoint(patient_id, experiment_id, body)
        ds.add_data(data_obj)

        # Instantly sync to your data.json file safely!
        ds.store_data() 
        return make_response('', 200)


if __name__ == '__main__':
    print('Starting service...')

    # load environmenta
    env_variables = load_environment()

    # check if there are data files for patients and experiments available
    ds = datastructure.DataStorage()
    ds.load_data()

    app.run(host='0.0.0.0', port=5001, debug=True)
