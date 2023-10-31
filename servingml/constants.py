import os


home_directory = os.path.expanduser("~")
SERVINGML_WORKING_DIR = os.path.join(home_directory, "servingml/svc")
MODEL_STORE_DIR = os.path.join(home_directory, "servingml/model_store")
MODEL_STORE_SKLEARN = os.path.join(MODEL_STORE_DIR, "sklearn")
MODEL_STORE_SKLEARN_WORKING = "./model_store/sklearn"
