# crypto_sentiments/common/trends/predict.py

import numpy as np
from sklearn import svm


class TrendPredictor(object):
    """
    """
    def __init__(self, training_set):
        """
        Params:
        - training_set [list[tuple]]: list of tuples of this form:
            (feature, label)
        """
        features = np.array([[f] for f, _ in training_set])
        labels = np.array([l for _, l in training_set])

        self._predictor = self._train(features, labels)

    @staticmethod
    def _train(features, labels):
        predictor = svm.SVC()
        predictor.fit(features, labels)
        return predictor

    def predict(self, feature):
        res = self._predictor.predict([[feature]])
        return res[0]
