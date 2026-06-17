import json
import os
import idgenerator

class Patient:
    def __init__(self, name, patient_id=None):
        self.name = name
        if patient_id is None:
            id_gen = idgenerator.AlphaNumericIDGenerator()
            self.id = id_gen.get_id()
        else:
            self.id = patient_id

    def to_dict(self):
        return self.__dict__

    def get_name(self):
        return self.name

class PatientEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Patient):
            return o.__dict__
        return super().default(o)


class Experiment:
    def __init__(self, name, experiment_id=None):
        self.name = name
        if experiment_id is None:
            id_gen = idgenerator.AlphaNumericIDGenerator()
            self.id = id_gen.get_id()
        else:
            self.id = experiment_id

    def to_dict(self):
        return self.__dict__

class ExperimentEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Experiment):
            return o.__dict__
        return super().default(o)


class DataPoint:
    def __init__(self, patient_id, experiment_id, data, dp_id=None):
        if dp_id is None:
            id_gen = idgenerator.AlphaNumericIDGenerator()
            self.id = id_gen.get_id()
        else:
            self.id = dp_id
        self.patient_id = patient_id
        self.experiment_id = experiment_id
        self.data = data

    def to_dict(self):
        return self.__dict__

class DataPointEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, DataPoint):
            return o.__dict__
        return super().default(o)


class DataStorage:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super().__new__(cls)
            cls.instance.experiments = {}
            cls.instance.patients = {}
            cls.instance.data = []
        return cls.instance

    def add_patient(self, obj):
        self.patients[obj.id] = obj

    def get_patient(self, patient_id):
        return self.patients.get(patient_id, None)

    def add_experiment(self, obj):
        self.experiments[obj.id] = obj

    def get_experiment(self, experiment_id):
        return self.experiments.get(experiment_id, None)

    def add_data(self, obj):
        self.data.append(obj)

    def store_data(self):
        # Convert dictionary values into serializable lists/structures
        patients_dict = {k: v.__dict__ for k, v in self.patients.items()}
        experiments_dict = {k: v.__dict__ for k, v in self.experiments.items()}
        
        with open('patients.json', 'w', encoding='utf-8') as pf:
            json.dump(patients_dict, pf, ensure_ascii=False, indent=4)
            
        with open('experiments.json', 'w', encoding='utf-8') as ef:
            json.dump(experiments_dict, ef, ensure_ascii=False, indent=4)
            
        with open('data.json', 'w', encoding='utf-8') as df:
            # Encodes list of DataPoint objects seamlessly
            json.dump(self.data, df, cls=DataPointEncoder, ensure_ascii=False, indent=4)

    def load_data(self):
        patient_file = 'patients.json'
        if os.path.exists(patient_file):
            with open(patient_file, encoding='utf-8') as file:
                patient_data = json.load(file)
            for val in patient_data.values():
                obj = Patient(val['name'], val['id'])
                self.patients[val['id']] = obj

        experiment_file = 'experiments.json'
        if os.path.exists(experiment_file):
            with open(experiment_file, encoding='utf-8') as file:
                experiment_data = json.load(file)
            for val in experiment_data.values():
                obj = Experiment(val['name'], val['id'])
                self.experiments[val['id']] = obj

        # FIX: Now properly loading existing Android data back into memory on startup
        data_file = 'data.json'
        if os.path.exists(data_file):
            with open(data_file, encoding='utf-8') as file:
                try:
                    loaded_data = json.load(file)
                    self.data = [
                        DataPoint(item['patient_id'], item['experiment_id'], item['data'], item['id'])
                        for item in loaded_data
                    ]
                except Exception as e:
                    print(f"Error parsing data.json: {e}")
                    self.data = []