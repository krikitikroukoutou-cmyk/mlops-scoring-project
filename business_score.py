import numpy as np
from sklearn.metrics import confusion_matrix, make_scorer

COUT_FN = 10
COUT_FP = 1

def cout_metier(y_true, y_pred):
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
    return fn * COUT_FN + fp * COUT_FP

def score_metier_normalise(y_true, y_pred):
    cout = cout_metier(y_true, y_pred)
    cout_max = len(y_true) * COUT_FN
    return 1 - (cout / cout_max)

scorer_metier = make_scorer(score_metier_normalise, greater_is_better=True)