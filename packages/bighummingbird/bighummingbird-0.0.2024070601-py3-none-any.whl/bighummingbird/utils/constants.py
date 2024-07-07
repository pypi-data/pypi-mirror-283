import os

BASE_URL=os.getenv("BIG_HUMMINGBIRD_API_URL") or "https://lyraml-api-2-7c3apmua4a-uc.a.run.app"
BASE_CLIENT_URL="http://localhost:3000"
PROJECT_BASE_URL = BASE_URL + "/projects"
RUN_BASE_URL = BASE_URL + "/runs"
MODEL_BASE_URL = BASE_URL + "/models"
DATASET_BASE_URL = BASE_URL + "/datasets"
JUDGE_BASE_URL = BASE_URL + "/judges"
EVALUATION_BASE_URL = BASE_URL + "/evaluations"