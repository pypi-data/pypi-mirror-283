"""
The :mod:`fairbalance.metrics` module includes fairness metrics for datasets, as well as the FairnessAnalysis class.
"""

from ._dataset_metrics import DIR, SPD, PMI, balance, balance_index, CBS
from ._model_metrics import evaluate_fairness_metric
from ._fairness_analysis import FairnessAnalysis

__all__ = [
    "DIR",
    "SPD",
    "PMI",
    "balance",
    "balance_index",
    "CBS",
    "FairnessAnalysis",
    "evaluate_fairness_metric"
]
