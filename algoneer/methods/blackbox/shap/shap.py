import shap
from typing import Iterable, Tuple, Optional
from algoneer import Dataset, Model, DatasetModelTest, Attribute, Datapoint
from algoneer.result import DatapointModelResult, DatasetModelResult, Result
from .force import force_plot

import numpy as np


class SHAPDatapointResult(Result):
    @property
    def name(self):
        return "shap.datapoint"

    @property
    def version(self):
        return "1.0.0"


class SHAPModelResult(Result):
    @property
    def name(self):
        return "shap.model"

    @property
    def version(self):
        return "1.0.0"


class SHAP(DatasetModelTest):

    """
    Generates SHAP explanations for a machine learning model.
    """

    def __init__(self):
        super().__init__()

    def run(self, dataset: Dataset, model: Model, **kwargs) -> DatasetModelResult:
        max_datapoints = kwargs.get("max_datapoints", None)
        npd = dataset.roles.x.df
        explainer = shap.KernelExplainer(model.predict, npd[:10])
        shap_values = explainer.shap_values(
            npd[:max_datapoints], l1_reg="num_features(10)"
        )
        ex = float(explainer.expected_value)
        dp_results = []
        for i, shap_value in enumerate(shap_values):
            dp_results.append(
                DatapointModelResult(
                    dataset.datapoint(i),
                    model,
                    SHAPDatapointResult(
                        {
                            "shap_value": shap_value.tolist(),
                            "columns": dataset.roles.x.columns,
                        }
                    ),
                )
            )
        plot_data = force_plot(np.array([ex]), shap_values, dataset.roles.x.df)
        return DatasetModelResult(
            dataset,
            model,
            SHAPModelResult(
                {
                    "expected_value": float(ex),
                    "shap_values": shap_values.tolist(),
                    "columns": list(dataset.roles.x.columns),
                    "plot_data": plot_data,
                }
            ),
            dp_results,
        )
