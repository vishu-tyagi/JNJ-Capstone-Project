import numpy as np

from sklearn.metrics import hamming_loss


class CustomEvaluation():
    def __init__(self):
        pass

    def hamming_eval(y_true: np.ndarray, y_pred: np.ndarray):
        return hamming_loss(y_true, y_pred)

    def exact_matching_ratio(y_true: np.ndarray, y_pred: np.ndarray):
        return np.mean(np.sum(y_true == y_pred, axis=1) / y_true.shape[1])
