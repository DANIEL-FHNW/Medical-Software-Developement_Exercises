import json
import idgenerator
import os

class Patient(object):
    """Description of class Patient"""
    def __init__(self, name, patient_id=None):
        self.name = name
        if patient_id is None:
            id_gen = idgenerator.AlphaNumericIDGenerator()
            self.id = id_gen.get_id()
        else:
            self.id = patient_id


class PatientEncoder(json.JSONEncoder):
    def default(self, obj):
        return obj.__dict__


class Experiment(object):
    def __init__(self, name, id=None):
        self.name = name
        if id is None:
            id_gen = idgenerator.AlphaNumericIDGenerator()
            self.id = id_gen.get_id()
        else:
            self.id = id


class ExperimentEncoder(json.JSONEncoder):
    def default(self, obj):
        return obj.__dict__


class DataPoint(object):
    def __init__(self, patient_id, experiment_id, data):
        id_gen = idgenerator.AlphaNumericIDGenerator()
        self.id = id_gen.get_id()
        self.patient_id = patient_id
        self.experiment_id = experiment_id
        self.data = data


class DataPointEncoder(json.JSONEncoder):
    def default(self, obj):
        return obj.__dict__


class DataStorage(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(DataStorage, cls).__new__(cls)
            cls.instance.experiments = {}
            cls.instance.patients = {}
            cls.instance.data = []
        return cls.instance

    def add_patient(self, obj):
        self.patients[obj.id] = obj

    def get_patient(self, id):
        if id in self.patients:
            return self.patients[id]
        else:
            return None

    def add_experiment(self, obj):
        self.experiments[obj.id] = obj

    def get_experiment(self, id):
        if id in self.experiments:
            return self.experiments[id]
        else:
            return None

    def add_data(self, obj):
        self.data.append(obj)

    def store_data(self):
        with open('patients.json', 'w') as pf:
            pf.write(json.dumps(self.patients, cls=PatientEncoder))
            pf.close()
        with open('experiments.json', 'w') as ef:
            ef.write(json.dumps(self.experiments, cls=ExperimentEncoder))
            ef.close()
        with open('data.json', 'w') as df:
            df.write(json.dumps(self.data, cls=DataPointEncoder))
            df.close()
        self.data.clear()

    def load_data(self):
        patient_file = 'patients.json'
        if os.path.exists(patient_file):
            with open(patient_file, 'r') as file:
                patient_data = json.load(file)
            for val in patient_data.values():
                obj = Patient(val['name'], val['id'])
                self.patients[val['id']] = obj

        experiment_file = 'experiments.json'
        if os.path.exists(experiment_file):
            with open(experiment_file, 'r') as file:
                experiment_data = json.load(file)
            for val in experiment_data.values():
                obj = Experiment(val['name'], val['id'])
                self.experiments[val['id']] = obj
