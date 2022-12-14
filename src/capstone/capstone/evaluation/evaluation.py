from typing import (List, Optional)

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from scipy.spatial.distance import cdist
from sklearn.metrics import (
    accuracy_score as _accuracy_score,
    precision_score as _precision_score,
    hamming_loss as _hamming_loss,
    zero_one_loss as _zero_one_loss,
    recall_score as _recall_score,
    f1_score as _f1_score,
    fbeta_score as _fbeta_score,
    multilabel_confusion_matrix
)

from capstone.config import CapstoneConfig
from capstone.features import Features
from capstone.utils.constants import (
    HAMMING_LOSS,
    ACCURACY,
    PRECISION,
    RECALL,
    F1_SCORE,
    F2_SCORE,
    CLUSTER,
    MAJORITY,
    SECOND_MAJORITY
)


class CustomEvaluation():
    def __init__(self, config: CapstoneConfig = CapstoneConfig):
        self.thresholds = [
            .1, .15, .2, .25, .3, .35, .4, .45, .5,
            .55, .6, .65, .7, .75, .8, .85, .9, .95
        ]

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

    def fbeta_score(self, y_true: np.ndarray, y_pred: np.ndarray, beta: np.float64):
        return _fbeta_score(
            y_true, y_pred, beta=beta, average="samples", zero_division=0
        )

    def compute_sample_wise_metrics(self, y_true: np.ndarray, y_pred: np.ndarray) -> pd.DataFrame:
        hamming_loss = self.hamming_loss(y_true, y_pred)
        accuracy = self.exact_matching_ratio(y_true, y_pred)
        precision_score = self.precision_score(y_true, y_pred)
        recall_score = self.recall_score(y_true, y_pred)
        f1_score = self.fbeta_score(y_true, y_pred, beta=1)
        f2_score = self.fbeta_score(y_true, y_pred, beta=2)
        scores = [hamming_loss, accuracy, precision_score, recall_score, f1_score, f2_score]
        metrics = [HAMMING_LOSS, ACCURACY, PRECISION, RECALL, F1_SCORE, F2_SCORE]
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
            f1_score = _fbeta_score(gt, predicted, beta=1, zero_division=0)
            f2_score = _fbeta_score(gt, predicted, beta=2, zero_division=0)
            row = [precision_score, recall_score, f1_score, f2_score]
            if dev_samples is not None:
                row.append(dev_samples[i])
            row.append(samples[i])
            scores.append(row)
        columns = [PRECISION, RECALL, F1_SCORE, F2_SCORE]
        if dev_samples is not None:
            columns.append("Development Samples")
        columns.append("Test Samples")
        df = pd.DataFrame(scores, index=labels, columns=columns)
        return df

    def threshold_discovery(self, y_true: np.ndarray, y_pred_probab: np.ndarray):
        n = y_true.shape[1]
        optimal_thresholds = []

        for j in range(n):
            gt = y_true[:, j].reshape(-1,)
            probab = y_pred_probab[:, j].reshape(-1,)

            score = _fbeta_score(gt, np.where(probab > .5, 1, 0), beta=2, zero_division=0)
            threshold = .5
            for th in self.thresholds:
                pred = np.where(probab > th, 1, 0)
                f2_score = _fbeta_score(gt, pred, beta=2, zero_division=0)
                if f2_score > score:
                    score = f2_score
                    threshold = th

            optimal_thresholds.append(threshold)

        return np.array(optimal_thresholds).reshape(-1,)

    def majority_vote(self, arr: List[str], minimum_votes: int) -> List[str]:
        d = {}
        for topic in arr:
            if topic in d:
                d[topic] += 1
            else:
                d[topic] = 1
        result = []
        for topic in d:
            if d[topic] >= minimum_votes:
                result.append(topic)
        return result

    def elbow_method(self, embeddings: np.ndarray, k_values: List):
        distortions = []
        inertias = []
        mapping1 = {}
        mapping2 = {}
        for k in k_values:
            kmeans = KMeans(n_clusters=k, random_state=0)
            kmeanModel = kmeans.fit(embeddings)
            distortions.append(
                sum(np.min(
                    cdist(embeddings, kmeanModel.cluster_centers_, "euclidean"),
                    axis=1
                )) / embeddings.shape[0]
            )
            inertias.append(kmeanModel.inertia_)
            mapping1[k] = sum(np.min(
                cdist(embeddings, kmeanModel.cluster_centers_, "euclidean"),
                axis=1
            )) / embeddings.shape[0]
            mapping2[k] = kmeanModel.inertia_
        return distortions, inertias

    def compute_purity_scores(
        self,
        clusters: np.ndarray,
        y_true: np.ndarray,
        topics: set(),
        features: Features
    ):
        rows = []
        labels_which_got_assigned = []
        for c in set(clusters.tolist()) - set({-1}):
            labels = y_true[clusters == c]
            labels_sorted = sorted(
                list(set(labels.tolist())),
                key=labels.tolist().count,
                reverse=True
            )
            most_common = labels_sorted[0]
            second_most_common = \
                labels_sorted[1] if len(labels_sorted) > 1 else -1
            max_purity = sum(labels == most_common) / len(labels)
            second_max_purity = \
                sum(labels == second_most_common) / len(labels) \
                if second_most_common != -1 else 0.0
            most_common_label = features.mlb.classes_[most_common]
            second_most_common_label = \
                features.mlb.classes_[second_most_common] \
                if second_most_common != -1 else -1
            rows.append([
                (most_common_label, f"{max_purity:.3}"),
                (second_most_common_label, f"{second_max_purity:.3}"),
                c
            ])
            labels_which_got_assigned.append(most_common_label)
        rows = sorted(rows, key=lambda x: x[0][0], reverse=False)
        df = pd.DataFrame(rows, columns=[MAJORITY, SECOND_MAJORITY, CLUSTER])
        counts = {}
        for label in labels_which_got_assigned:
            counts[label] = 1 if label not in counts else (counts[label] + 1)
        missing = topics - set(counts.keys())
        multiple = [(label, counts[label]) for label in counts if counts[label] > 1]
        return df, missing, multiple

    def sanity_check(self, scores: dict()):
        counts = {}
        for c in scores:
            if scores[c][1] not in counts:
                counts[scores[c][1]] = 1
            else:
                counts[scores[c][1]] += 1
        missing = set(features.mlb.classes_) - set([c for c in counts])
        multiple = [(c, counts[c]) for c in counts if counts[c] > 1]
        return missing, multiple