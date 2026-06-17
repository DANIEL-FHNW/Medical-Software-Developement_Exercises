import json
import pytest
from unittest.mock import MagicMock, patch

#UNITY TESTS FOR app.py >> independently from datastructure.py > mocking all interactions with DataStorage and related classes

@pytest.fixture
def mock_patient():
    patient = MagicMock()
    patient.id = "p-001"
    patient.name = "Alice"
    patient.__dict__ = {"id": "p-001", "name": "Alice"}
    return patient


@pytest.fixture
def mock_experiment():
    experiment = MagicMock()
    experiment.id = "e-001"
    experiment.name = "Trial A"
    experiment.__dict__ = {"id": "e-001", "name": "Trial A"}
    return experiment


@pytest.fixture
def client(mock_patient, mock_experiment):
   
    mock_ds = MagicMock()
    mock_ds.get_patient.return_value = mock_patient
    mock_ds.get_experiment.return_value = mock_experiment
    mock_ds.patients = [mock_patient]
    mock_ds.experiments = [mock_experiment]

    with patch("datastructure.DataStorage", return_value=mock_ds), \
         patch("datastructure.Patient", return_value=mock_patient), \
         patch("datastructure.Experiment", return_value=mock_experiment), \
         patch("datastructure.DataPoint", return_value=MagicMock()), \
         patch("datastructure.PatientEncoder"), \
         patch("datastructure.ExperimentEncoder"):

        from app import app
        app.config["TESTING"] = True
        with app.test_client() as c:
            yield c


#GET /

class TestIndex:
    def test_returns_200(self, client):
        res = client.get("/")
        assert res.status_code == 200

    def test_response_contains_required_fields(self, client):
        body = json.loads(client.get("/").data)
        assert "name" in body
        assert "System" in body
        assert "Server Component" in body

    def test_response_time_below_threshold(self, client):
        import time
        start = time.time()
        client.get("/")
        elapsed_ms = (time.time() - start) * 1000
        assert elapsed_ms < 500, f"Response took {elapsed_ms:.1f} ms — exceeded 500 ms threshold"

#POST /patient

class TestCreatePatient:
    def test_returns_200(self, client):
        res = client.post("/patient", json={"name": "Alice"})
        assert res.status_code == 200

    def test_response_contains_id_and_name(self, client):
        body = client.post("/patient", json={"name": "Alice"}).get_json()
        assert "id" in body
        assert "name" in body

    def test_missing_name_returns_400(self, client):
        res = client.post("/patient", json={})
        assert res.status_code == 400

#GET /patient

class TestGetPatient:
    def test_returns_200_for_existing_id(self, client):
        res = client.get("/patient?id=p-001")
        assert res.status_code == 200

    def test_returns_404_for_missing_id(self, client, mock_ds=None):
        with patch("datastructure.DataStorage") as MockDS:
            MockDS.return_value.get_patient.return_value = None
            res = client.get("/patient?id=does-not-exist")
            assert res.status_code == 404

    def test_response_contains_id_and_name(self, client):
        body = client.get("/patient?id=p-001").get_json()
        assert "id" in body
        assert "name" in body


#POST /experiment

class TestCreateExperiment:
    def test_returns_200(self, client):
        res = client.post("/experiment", json={"name": "Trial A"})
        assert res.status_code == 200

    def test_response_contains_id_and_name(self, client):
        body = client.post("/experiment", json={"name": "Trial A"}).get_json()
        assert "id" in body
        assert "name" in body

    def test_missing_name_returns_400(self, client):
        res = client.post("/experiment", json={})
        assert res.status_code == 400


#GET /experiment

class TestGetExperiment:
    def test_returns_200_for_existing_id(self, client):
        res = client.get("/experiment?id=e-001")
        assert res.status_code == 200

    def test_returns_404_for_missing_id(self, client):
        with patch("datastructure.DataStorage") as MockDS:
            MockDS.return_value.get_experiment.return_value = None
            res = client.get("/experiment?id=does-not-exist")
            assert res.status_code == 404

#POST /upload

class TestUploadData:
    def test_returns_200(self, client):
        res = client.post("/upload", json={
            "patientId": "p-001",
            "experimentId": "e-001",
            "value": 1.23,
            "unit": "mg/dL"
        })
        assert res.status_code == 200

    def test_missing_patient_id_returns_400(self, client):
        res = client.post("/upload", json={
            "experimentId": "e-001",
            "value": 1.23
        })
        assert res.status_code == 400


#POST /store

class TestStoreData:
    def test_returns_200(self, client):
        res = client.post("/store")
        assert res.status_code == 200


#GET /patients and GET /experiments

class TestListEndpoints:
    def test_get_patients_returns_200(self, client):
        res = client.get("/patients")
        assert res.status_code == 200

    def test_get_experiments_returns_200(self, client):
        res = client.get("/experiments")
        assert res.status_code == 200

