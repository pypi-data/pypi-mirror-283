from fairbalance.tests.base_test import BaseSetUp
from fairlearn.metrics import demographic_parity_ratio
from fairbalance.metrics import evaluate_fairness_metric
import pytest


class TestBaseMetrics(BaseSetUp):

    def test_evaluate_fairness_metrics(self):
        self.setUp()

        mean = evaluate_fairness_metric(self.target.squeeze(),
                                        self.prediction.squeeze(),
                                        self.dataset[[
                                            self.protected_attributes[0]]],
                                        demographic_parity_ratio, "mean")

        min_ = evaluate_fairness_metric(self.target.squeeze(),
                                        self.prediction.squeeze(),
                                        self.dataset[[
                                            self.protected_attributes[0]]],
                                        demographic_parity_ratio, "min")

        max_ = evaluate_fairness_metric(self.target.squeeze(),
                                        self.prediction.squeeze(),
                                        self.dataset[[
                                            self.protected_attributes[0]]],
                                        demographic_parity_ratio, "max")

        median = evaluate_fairness_metric(self.target.squeeze(),
                                          self.prediction.squeeze(),
                                          self.dataset[[
                                              self.protected_attributes[0]]],
                                          demographic_parity_ratio, "median")

        with pytest.raises(ValueError):
            wrong_eval = evaluate_fairness_metric(self.target.squeeze(),
                                                  self.prediction.squeeze(),
                                                  self.dataset[[
                                                      self.protected_attributes[0]]],
                                                  demographic_parity_ratio, "wrong_eval")
