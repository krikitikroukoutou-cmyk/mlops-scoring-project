import pandas as pd
import mlflow
import mlflow.sklearn
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import roc_auc_score, classification_report
from imblearn.over_sampling import SMOTE
import shap
import joblib
import matplotlib.pyplot as plt

from business_score import scorer_metier

mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("scoring-credit")

X_train = pd.read_csv("data/X_train.csv")
X_test = pd.read_csv("data/X_test.csv")
y_train = pd.read_csv("data/y_train.csv").values.ravel()
y_test = pd.read_csv("data/y_test.csv").values.ravel()

sm = SMOTE(random_state=42)
X_train_res, y_train_res = sm.fit_resample(X_train, y_train)

modeles = {
    "logistic_regression": (LogisticRegression(max_iter=1000), {"C": [0.01, 0.1, 1, 10]}),
    "random_forest": (RandomForestClassifier(random_state=42), {"n_estimators": [100, 200], "max_depth": [5, 10, None]}),
    "xgboost": (XGBClassifier(eval_metric="logloss", random_state=42), {"n_estimators": [100, 200], "max_depth": [3, 6]}),
}

meilleur_score = -1
meilleur_modele_nom = None
meilleur_modele_obj = None

for nom, (modele, params) in modeles.items():
    with mlflow.start_run(run_name=nom):
        grid = GridSearchCV(modele, params, scoring=scorer_metier, cv=3, n_jobs=-1)
        grid.fit(X_train_res, y_train_res)

        best = grid.best_estimator_
        y_pred = best.predict(X_test)
        y_proba = best.predict_proba(X_test)[:, 1]

        auc = roc_auc_score(y_test, y_proba)
        score_business = scorer_metier(best, X_test, y_test)

        mlflow.log_params(grid.best_params_)
        mlflow.log_metric("auc", auc)
        mlflow.log_metric("score_metier", score_business)
        mlflow.sklearn.log_model(best, nom)

        print(f"{nom} -> AUC: {auc:.3f} | Score métier: {score_business:.3f}")
        print(classification_report(y_test, y_pred))

        if score_business > meilleur_score:
            meilleur_score = score_business
            meilleur_modele_nom = nom
            meilleur_modele_obj = best

print(f"\nMeilleur modèle : {meilleur_modele_nom} (score métier = {meilleur_score:.3f})")

joblib.dump(meilleur_modele_obj, "model.pkl")

explainer = shap.Explainer(meilleur_modele_obj, X_train_res)
shap_values = explainer(X_test[:200])
shap.summary_plot(shap_values, X_test[:200], show=False)
plt.savefig("shap_summary.png", bbox_inches="tight")
mlflow.log_artifact("shap_summary.png")