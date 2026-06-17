from locust import HttpUser, task, between, events
import random
import string
import logging
import os
from datetime import datetime

#LOGGING SETUP
LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
os.makedirs(LOG_DIR, exist_ok=True)

#Ccreate logfile with timestamp
log_filename = os.path.join(LOG_DIR, f"locust_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(log_filename),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


# locust event listeners for test start/stop to log summary stats and test lifecycle events
@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    logger.info("Performance test started | Log: %s", log_filename)


@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    stats = environment.stats.total
    logger.info(
        "Performance test finished | Requests: %d | Failures: %d | "
        "Avg response: %.1f ms | RPS: %.2f",
        stats.num_requests,
        stats.num_failures,
        stats.avg_response_time,
        stats.current_rps
    )


def random_name():
    return ''.join(random.choices(string.ascii_lowercase, k=8))


# ASSERTION THRESHOLDS
MAX_RESPONSE_MS = 500   # >>every endpoint must respond within 500 ms
REQUIRED_KEYS = {
    "/patient":    ["id", "name"],
    "/experiment": ["id", "name"],
}


def assert_response(res, endpoint, expected_status=200):
    """
    Central assertion helper — checks status code, response time, and
    required JSON fields. Marks the request as failed in Locust if any
    assertion fails and logs the violation.
    """
    elapsed_ms = res.elapsed.total_seconds() * 1000
    errors = []

    # 1. Status code
    if res.status_code != expected_status:
        errors.append(f"expected status {expected_status}, got {res.status_code}")

    # 2. Response time
    if elapsed_ms > MAX_RESPONSE_MS:
        errors.append(f"response time {elapsed_ms:.1f} ms exceeded {MAX_RESPONSE_MS} ms")

    # 3. Required JSON fields
    if not errors and endpoint in REQUIRED_KEYS:
        try:
            body = res.json()
            for key in REQUIRED_KEYS[endpoint]:
                if key not in body:
                    errors.append(f"missing field '{key}' in response body")
        except Exception:  # pylint: disable=broad-except
            errors.append("response body is not valid JSON")

    if errors:
        msg = " | ".join(errors)
        res.failure(msg)
        logger.error("ASSERTION FAILED | %s | %s", endpoint, msg)
        return False

    logger.debug("OK | %s | status=%d | %.1f ms", endpoint, res.status_code, elapsed_ms)
    return True


class APIUser(HttpUser):
    host = "http://10.207.22.188:5001"
    wait_time = between(1, 3)

    patient_ids = []
    experiment_ids = []

    def on_start(self):
        """Called once per simulated user on startup — seeds IDs for GET/upload tasks."""
        p_res = self.client.post("/patient", json={"name": random_name()})
        if p_res.status_code == 200:
            pid = p_res.json().get("id")
            self.patient_ids.append(pid)
            logger.info("Seeded patient | id=%s", pid)
        else:
            logger.warning("Failed to seed patient | status=%d", p_res.status_code)

        e_res = self.client.post("/experiment", json={"name": random_name()})
        if e_res.status_code == 200:
            eid = e_res.json().get("id")
            self.experiment_ids.append(eid)
            logger.info("Seeded experiment | id=%s", eid)
        else:
            logger.warning("Failed to seed experiment | status=%d", e_res.status_code)

    # --- GET endpoints ---

    @task(3)
    def get_index(self):
        with self.client.get("/", catch_response=True) as res:
            assert_response(res, "/")

    @task(3)
    def get_all_patients(self):
        with self.client.get("/patients", catch_response=True) as res:
            assert_response(res, "/patients")

    @task(3)
    def get_all_experiments(self):
        with self.client.get("/experiments", catch_response=True) as res:
            assert_response(res, "/experiments")

    @task(2)
    def get_patient_by_id(self):
        if self.patient_ids:
            pid = random.choice(self.patient_ids)
            with self.client.get(f"/patient?id={pid}", catch_response=True) as res:
                if res.status_code == 404:
                    res.failure("Patient not found")
                    logger.warning("GET /patient | NOT FOUND | id=%s", pid)
                else:
                    assert_response(res, "/patient")

    @task(2)
    def get_experiment_by_id(self):
        if self.experiment_ids:
            eid = random.choice(self.experiment_ids)
            with self.client.get(f"/experiment?id={eid}", catch_response=True) as res:
                if res.status_code == 404:
                    res.failure("Experiment not found")
                    logger.warning("GET /experiment | NOT FOUND | id=%s", eid)
                else:
                    assert_response(res, "/experiment")

    # --- POST endpoints ---

    @task(2)
    def create_patient(self):
        with self.client.post("/patient", json={"name": random_name()}, catch_response=True) as res:
            if assert_response(res, "/patient"):
                pid = res.json().get("id")
                self.patient_ids.append(pid)
                logger.info("POST /patient | Created | id=%s", pid)

    @task(2)
    def create_experiment(self):
        with self.client.post("/experiment", json={"name": random_name()}, catch_response=True) as res:
            if assert_response(res, "/experiment"):
                eid = res.json().get("id")
                self.experiment_ids.append(eid)
                logger.info("POST /experiment | Created | id=%s", eid)

    @task(2)
    def upload_data(self):
        if self.patient_ids and self.experiment_ids:
            pid = random.choice(self.patient_ids)
            eid = random.choice(self.experiment_ids)
            with self.client.post("/upload", json={
                "patientId": pid,
                "experimentId": eid,
                "value": round(random.uniform(0.5, 5.0), 3),
                "unit": "mg/dL"
            }, catch_response=True) as res:
                assert_response(res, "/upload")

    @task(1)
    def store_data(self):
        """Lower weight — triggers persistence, heavier operation."""
        with self.client.post("/store", catch_response=True) as res:
            assert_response(res, "/store")