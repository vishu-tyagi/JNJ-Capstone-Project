from typing import (List, Optional)

import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score as _accuracy_score,
    precision_score as _precision_score,
    hamming_loss as _hamming_loss,
    zero_one_loss as _zero_one_loss,
    recall_score as _recall_score,
    f1_score as _f1_score,
    multilabel_confusion_matrix
)

from capstone.config import CapstoneConfig
from capstone.utils.constants import (
    HAMMING_LOSS,
    ACCURACY,
    PRECISION,
    RECALL,
    F1_SCORE
)


class CustomEvaluation():
    def __init__(self, config: CapstoneConfig = CapstoneConfig):
        pass

    def hamming_loss(self, y_true: np.ndarray, y_pred: np.ndarray):
        return _hamming_loss(y_true, y_pred)

    def zero_one_loss(self, y_true: np.ndarray, y_pred: np.ndarray):
        # This is (1 - exact_matching_ratio)
        return _zero_one_loss(y_true, y_pred)

    def exact_matching_ratio(self, y_true: np.ndarray, y_pred: np.ndarray):
        return _accuracy_score(y_true, y_pred)

    def precision_score(self, y_true: np.ndarray, y_pred: np.ndarray):
        return _precision_score(
            y_true, y_pred, average="samples", zero_division=0
        )

    def recall_score(self, y_true: np.ndarray, y_pred: np.ndarray):
        return _recall_score(
            y_true, y_pred, average="samples", zero_division=0
        )

    def f1_score(self, y_true: np.ndarray, y_pred: np.ndarray):
        return _f1_score(
            y_true, y_pred, average="samples", zero_division=0
        )

    def compute_sample_wise_metrics(self, y_true: np.ndarray, y_pred: np.ndarray) -> pd.DataFrame:
        hamming_loss = self.hamming_loss(y_true, y_pred)
        accuracy = self.exact_matching_ratio(y_true, y_pred)
        precision_score = self.precision_score(y_true, y_pred)
        recall_score = self.recall_score(y_true, y_pred)
        f1_score = self.f1_score(y_true, y_pred)
        scores = [hamming_loss, accuracy, precision_score, recall_score, f1_score]
        metrics = [HAMMING_LOSS, ACCURACY, PRECISION, RECALL, F1_SCORE]
        return pd.Series(data=scores, index=metrics)

    def compute_multilabel_confusion_matrix(
        self,
        y_true: np.ndarray,
        y_pred: np.ndarray,
        labels: List[str]
    ) -> pd.DataFrame:
        multi_confusion_matirx = multilabel_confusion_matrix(y_true, y_pred)
        df = pd.DataFrame(
            [[(
                pd.DataFrame(x)
                .style
                .hide_index()
                .hide_columns()
                .set_table_attributes("class='matrix'")
                .to_html()
            ) for x in multi_confusion_matirx]],
            columns=labels,
            index=[
                pd.DataFrame(np.array([["TN", "FP"], ["FN", "TP"]]))
                .style
                .hide_index()
                .hide_columns()
                .set_table_attributes("class='matrix'")
                .to_html()
            ],
            dtype="object"
        ).T
        return df

    def compute_label_wise_metrics(
        self,
        y_true: np.ndarray,
        y_pred: np.ndarray,
        labels: List[str],
        dev_samples: Optional[List[int]] = None
    ) -> pd.DataFrame:
        samples = y_true.sum(axis=0).tolist()
        scores = []
        for i, label in enumerate(labels):
            gt = y_true[:, i]
            predicted = y_pred[:, i]
            precision_score = _precision_score(gt, predicted, zero_division=0)
            recall_score = _recall_score(gt, predicted, zero_division=0)
            f1_score = _f1_score(gt, predicted, zero_division=0)
            row = [precision_score, recall_score, f1_score]
            if dev_samples is not None:
                row.append(dev_samples[i])
            row.append(samples[i])
            scores.append(row)
        columns = [PRECISION, RECALL, F1_SCORE]
        if dev_samples is not None:
            columns.append("Development Samples")
        columns.append("Test Samples")
        df = pd.DataFrame(scores, index=labels, columns=columns)
        return df
