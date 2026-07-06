import mlflow

mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("test-experiment")

with mlflow.start_run():
    mlflow.log_param("alpha", 0.5)
    mlflow.log_metric("accuracy", 0.87)
    with open("note.txt", "w") as f:
        f.write("Ceci est un artefact de test")
    mlflow.log_artifact("note.txt")

print("Run enregistré avec succès.")