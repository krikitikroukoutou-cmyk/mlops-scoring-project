import pandas as pd
from evidently import Report
from evidently.presets import DataDriftPreset

X_train = pd.read_csv("data/X_train.csv")
X_test = pd.read_csv("data/X_test.csv")  # à remplacer par de nouvelles données de production

report = Report([DataDriftPreset()])
my_eval = report.run(current_data=X_test, reference_data=X_train)
my_eval.save_html("data_drift_report.html")
print("Rapport de drift généré : data_drift_report.html")