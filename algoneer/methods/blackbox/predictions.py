"""
algoneer.methods.blackbox.pdp
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This modules implements the generation of partial dependence plots for machine
learning models.
"""

from typing import Iterable, Any, Dict
from algoneer import Dataset, Model, ModelTest, Attribute, Datapoint
from algoneer.result import ModelResult, DatapointModelResult


class PredictionsDatapointResult(DatapointModelResult):
    @property
    def name(self):
        return "predictions.datapoint"

    @property
    def version(self):
        return "1.0.0"


class PredictionsResult(ModelResult):
    @property
    def name(self):
        return "predictions.model"

    @property
    def version(self):
        return "1.0.0"


class Predictions(ModelTest):

    """
    Generates a list of predictions for a given model.
    """

    def __init__(self):
        super().__init__()

    def run(self, model: Model, dataset: Dataset, **kwargs) -> ModelResult:
        max_datapoints = kwargs.get("max_datapoints", None)
        Y = model.predict(dataset)
        results = []
        for y in Y:
            ind, pred = y
            dp = dataset.datapoint(ind)
            results.append(PredictionsDatapointResult({"p": float(pred)}, dp, model))

        return PredictionsResult({}, model, results)
