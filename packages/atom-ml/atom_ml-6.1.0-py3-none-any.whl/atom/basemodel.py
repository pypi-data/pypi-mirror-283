"""Automated Tool for Optimized Modeling (ATOM).

Author: Mavs
Description: Module containing the BaseModel class.

"""

from __future__ import annotations

import re
from collections import defaultdict
from copy import deepcopy
from datetime import datetime as dt
from functools import cached_property
from importlib import import_module
from logging import Logger
from pathlib import Path
from typing import TYPE_CHECKING, Any, Literal, cast, overload
from unittest.mock import patch

import dill as pickle
import mlflow
import numpy as np
import optuna
import pandas as pd
from beartype import beartype
from joblib.memory import Memory
from joblib.parallel import Parallel, delayed
from mlflow.data import from_pandas
from mlflow.entities import Run
from mlflow.models.signature import infer_signature
from mlflow.tracking import MlflowClient
from optuna import TrialPruned, create_study
from optuna.samplers import NSGAIISampler, TPESampler
from optuna.storages import InMemoryStorage
from optuna.study import Study
from optuna.terminator import report_cross_validation_scores
from optuna.trial import FrozenTrial, Trial, TrialState
from pandas.io.formats.style import Styler
from sklearn.base import clone
from sklearn.calibration import CalibratedClassifierCV
from sklearn.model_selection import (
    BaseCrossValidator, FixedThresholdClassifier, GroupKFold,
    GroupShuffleSplit, KFold, ShuffleSplit, StratifiedGroupKFold,
    StratifiedKFold, StratifiedShuffleSplit, TunedThresholdClassifierCV,
)
from sklearn.model_selection._validation import cross_validate
from sklearn.multioutput import (
    ClassifierChain, MultiOutputClassifier, MultiOutputRegressor,
)
from sklearn.utils import resample
from sklearn.utils.metaestimators import available_if
from sklearn.utils.validation import _check_response_method
from sktime.forecasting.base import BaseForecaster, ForecastingHorizon
from sktime.forecasting.compose import make_reduction
from sktime.forecasting.model_evaluation import evaluate
from sktime.performance_metrics.forecasting import make_forecasting_scorer
from sktime.proba.normal import Normal
from sktime.split import ExpandingWindowSplitter, SingleWindowSplitter

from atom.data import Branch, BranchManager
from atom.data_cleaning import Scaler
from atom.pipeline import Pipeline
from atom.plots import RunnerPlot
from atom.utils.constants import COLOR_SCHEME, DF_ATTRS
from atom.utils.patches import fit_and_score
from atom.utils.types import (
    HT, Backend, Bool, Engine, Float, Int, IntLargerEqualZero,
    MetricConstructor, MetricFunction, NJobs, Pandas, PredictionMethods,
    PredictionMethodsTS, Predictor, RowSelector, Scalar, Scorer, Sequence,
    Stages, TargetSelector, Verbose, Warnings, XReturn, XSelector,
    YConstructor, YReturn, YSelector, int_t,
)
from atom.utils.utils import (
    ClassMap, DataConfig, Goal, PlotCallback, ShapExplanation, Task,
    TrialsCallback, adjust, cache, check_dependency, check_empty, composed,
    crash, estimator_has_attr, get_cols, get_custom_scorer, has_task,
    is_sparse, it, lst, merge, method_to_log, rnd, sign, time_to_str, to_df,
    to_series, to_tabular,
)


if TYPE_CHECKING:
    from starlette.requests import Request


# Disable optuna info logs (ATOM already displays the same info)
optuna.logging.set_verbosity(optuna.logging.WARNING)


class BaseModel(RunnerPlot):
    """Base class for all models.

    Parameters
    ----------
    goal: Goal
        Model's goal (classification, regression or forecast).

    name: str or None, default=None
        Name for the model. If None, the name is the same as the
        model's acronym.

    config: DataConfig or None, default=None
        Data configuration. If None, use the default config values.

    branches: BranchManager or None, default=None
        BranchManager.

    metric: ClassMap or None, default=None
        Metric on which to fit the model.

    n_jobs: int, default=1
        Number of cores to use for parallel processing.

        - If >0: Number of cores to use.
        - If -1: Use all available cores.
        - If <-1: Use number of cores - 1 + `n_jobs`.

    device: str, default="cpu"
        Device on which to run the estimators. Use any string that
        follows the [SYCL_DEVICE_FILTER][] filter selector, e.g.
        `#!python device="gpu"` to use the GPU. Read more in the
        [user guide][gpu-acceleration].

    engine: str, dict or None, default=None
        Execution engine to use for [data][data-engines] and
        [estimators][estimator-acceleration]. The value should be
        one of the possible values to change one of the two engines,
        or a dictionary with keys `data` and `estimator`, with their
        corresponding choice as values to change both engines. If
        None, the default values are used. Choose from:

        - "data":

            - "numpy"
            - "pandas" (default)
            - "pandas-pyarrow"
            - "polars"
            - "polars-lazy"
            - "pyarrow"
            - "modin"
            - "dask"
            - "pyspark"
            - "pyspark-pandas"

        - "estimator":

            - "sklearn" (default)
            - "sklearnex"
            - "cuml"

    backend: str, default="loky"
        Parallelization backend. Read more in the
        [user guide][parallel-execution]. Choose from:

        - "loky": Single-node, process-based parallelism.
        - "multiprocessing": Legacy single-node, process-based
          parallelism. Less robust than `loky`.
        - "threading": Single-node, thread-based parallelism.
        - "ray": Multi-node, process-based parallelism.
        - "dask": Multi-node, process-based parallelism.

    memory: bool, str, Path or Memory, default=False
        Enables caching for memory optimization. Read more in the
        [user guide][memory-considerations].

        - If False: No caching is performed.
        - If True: A default temp directory is used.
        - If str: Path to the caching directory.
        - If Path: A [pathlib.Path][] to the caching directory.
        - If Memory: Object with the [joblib.Memory][] interface.

    verbose: int, default=0
        Verbosity level of the class. Choose from:

        - 0 to not print anything.
        - 1 to print basic information.
        - 2 to print detailed information.

    warnings: bool or str, default=False
        - If True: Default warning action (equal to "once").
        - If False: Suppress all warnings (equal to "ignore").
        - If str: One of python's [warnings filters][warnings].

        Changing this parameter affects the `PYTHONWarnings` environment.
        ATOM can't manage warnings that go from C/C++ code to stdout.

    logger: str, Logger or None, default=None
        - If None: Logging isn't used.
        - If str: Name of the log file. Use "auto" for automatic name.
        - If Path: A [pathlib.Path][] to the log file.
        - Else: Python `logging.Logger` instance.

    experiment: str or None, default=None
        Name of the [mlflow experiment][experiment] to use for tracking.
        If None, no mlflow tracking is performed.

    random_state: int or None, default=None
        Seed used by the random number generator. If None, the random
        number generator is the `RandomState` used by `np.random`.

    """

    def __init__(
        self,
        goal: Goal,
        name: str | None = None,
        config: DataConfig | None = None,
        branches: BranchManager | None = None,
        metric: ClassMap | None = None,
        *,
        n_jobs: NJobs = 1,
        device: str = "cpu",
        engine: Engine = None,
        backend: Backend = "loky",
        memory: Bool | str | Path | Memory = False,
        verbose: Verbose = 0,
        warnings: Bool | Warnings = False,
        logger: str | Path | Logger | None = None,
        experiment: str | None = None,
        random_state: IntLargerEqualZero | None = None,
    ):
        super().__init__(
            n_jobs=n_jobs,
            device=device,
            engine=engine,
            backend=backend,
            memory=memory,
            verbose=verbose,
            warnings=warnings,
            logger=logger,
            experiment=experiment,
            random_state=random_state,
        )

        self._goal = goal
        self._name = name or self.acronym

        self._config = config or DataConfig()
        self._metric = metric or ClassMap()

        self.scaler: Scaler | None = None

        if self.experiment:
            self._run = mlflow.start_run(run_name=self.name)
            mlflow.end_run()

        self._group = self._name  # sh and ts models belong to the same group
        self._evals: dict[str, list[Float]] = defaultdict(list)
        self._shap_explanation: ShapExplanation | None = None

        # Parameter attributes
        self._est_params: dict[str, Any] = {}
        self._est_params_fit: dict[str, Any] = {}

        # Hyperparameter tuning attributes
        self._ht: HT = {"distributions": {}, "cv": 1, "plot": False, "tags": {}}
        self._study: Study | None = None
        self._best_trial: FrozenTrial | None = None

        self._estimator: Predictor | None = None
        self._time_fit = 0.0

        self._bootstrap: pd.DataFrame | None = None
        self._time_bootstrap = 0.0

        # Inject goal-specific methods from ForecastModel
        if goal is Goal.forecast and ClassRegModel in self.__class__.__bases__:
            for n, m in vars(ForecastModel).items():
                if hasattr(m, "__get__"):
                    setattr(self, n, m.__get__(self, ForecastModel))

        # Skip this part if only initialized for the estimator
        if branches:
            self._og = branches.og
            self._branch = branches.current
            self._train_idx = len(self.branch._data.train_idx)  # Can change for sh and ts

            if getattr(self, "needs_scaling", None) and not self.branch.check_scaling():
                self.scaler = Scaler(
                    with_mean=not is_sparse(self.X_train),
                    device=self.device,
                    engine=self.engine.estimator,
                ).fit(self.X_train)

    def __repr__(self) -> str:
        """Display class name."""
        return f"{self.__class__.__name__}()"

    def __dir__(self) -> list[str]:
        """Add additional attrs from __getattr__ to the dir."""
        # Exclude from _available_if conditions
        attrs = [x for x in super().__dir__() if hasattr(self, x)]

        if "_branch" in self.__dict__:
            # Add additional attrs from the branch
            attrs += self.branch._get_shared_attrs()

            # Add additional attrs from the dataset
            attrs += [x for x in DF_ATTRS if hasattr(self.dataset, x)]

            # Add column names (excluding those with spaces)
            attrs += [c for c in self.columns if re.fullmatch(r"\w+$", c)]

        return attrs

    def __getattr__(self, item: str) -> Any:
        """Get attributes from branch or data."""
        if "_branch" in self.__dict__:
            if item in self.branch._get_shared_attrs():
                return getattr(self.branch, item)  # Get attr from branch
            elif item in self.branch.columns:
                return self.branch.dataset[item]  # Get column
            elif item in DF_ATTRS:
                return getattr(self.branch.dataset, item)  # Get attr from dataset

        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{item}'.")

    def __contains__(self, item: str) -> bool:
        """Whether the item is a column in the dataset."""
        return item in self.dataset

    def __getitem__(self, item: Int | str | list) -> Pandas:
        """Get a subset from the dataset."""
        if isinstance(item, int_t):
            return self.dataset[self.columns[int(item)]]
        else:
            return self.dataset[item]  # Get a subset of the dataset

    @property
    def fullname(self) -> str:
        """Return the model's class name."""
        return self.__class__.__name__

    @cached_property
    def _est_class(self) -> type[Predictor]:
        """Return the estimator's class (not instance).

        This property checks which estimator engine is enabled and
        retrieves the model's estimator from the right library.

        """
        locator = self._estimators.get(self._goal.name, self._estimators.get("regression"))
        module, est_name = locator.rsplit(".", 1)

        # Try engine, else import from the default module
        try:
            mod = import_module(f"{self.engine.estimator}.{module.split('.', 1)[1]}")
        except (ModuleNotFoundError, AttributeError, IndexError):
            mod = import_module(module)

        return getattr(mod, est_name)

    @property
    def _shap(self) -> ShapExplanation:
        """Return the ShapExplanation instance for this model."""
        if not self._shap_explanation:
            self._shap_explanation = ShapExplanation(
                estimator=self.estimator,
                task=self.task,
                branch=self.branch,
                random_state=self.random_state,
            )

        return self._shap_explanation

    def _check_est_params(self):
        """Check that the parameters are valid for the estimator.

        A parameter is always accepted if the method accepts kwargs.

        """
        for param in self._est_params:
            if all(p not in sign(self._est_class) for p in (param, "kwargs")):
                raise ValueError(
                    "Invalid value for the est_params parameter. Got unknown "
                    f"parameter {param} for estimator {self._est_class.__name__}."
                )

        for param in self._est_params_fit:
            if all(p not in sign(self._est_class.fit) for p in (param, "kwargs")):
                raise ValueError(
                    f"Invalid value for the est_params parameter. Got "
                    f"unknown parameter {param} for the fit method of "
                    f"estimator {self._est_class.__name__}."
                )

    def _get_param(self, name: str, params: dict[str, Any]) -> Any:
        """Get a parameter from est_params or the objective func.

        Parameters
        ----------
        name: str
            Name of the parameter.

        params: dict
            Parameters in the current trial.

        Returns
        -------
        Any
            Parameter value.

        """
        return self._est_params.get(name) or params.get(name)

    def _get_parameters(self, trial: Trial) -> dict[str, Any]:
        """Get the trial's hyperparameters.

        This method fetches the suggestions from the trial and
        rounds floats to the fourth digit.

        Parameters
        ----------
        trial: [Trial][]
            Current trial.

        Returns
        -------
        dict
            Trial's hyperparameters.

        """
        return {
            parameter: rnd(trial._suggest(parameter, value))
            for parameter, value in self._ht["distributions"].items()
        }

    def _trial_to_est(self, params: dict[str, Any]) -> dict[str, Any]:
        """Convert trial's parameters to parameters for the estimator.

        Some models, such as MLP, use different hyperparameters for the
        study as for the estimator (this is the case when the estimator's
        parameter cannot be modeled according to an integer, float or
        categorical distribution). This method converts the parameters
        from the trial to those that can be ingested by the estimator.
        This method is overriden by implementations in the child classes.
        The base method just returns the parameters as is.

        Parameters
        ----------
        params: dict
            Trial's hyperparameters.

        Returns
        -------
        dict
            Copy of the estimator's hyperparameters.

        """
        return deepcopy(params)

    def _get_cv(self, cv: Int | BaseCrossValidator, max_length: Int) -> BaseCrossValidator:
        """Return a cross-validator class.

        The cross-validator is selected based on the task and the
        presence/absence of groups and stratification.

        Parameters
        ----------
        cv: int or CrossValidator
            Number of folds or cv object. If cv object, it is returned
            as is.

        total_length: int
            Total length of the dataset. Only used for forecasting
            tasks when cv > 1.

        Returns
        -------
        CrossValidator
            Cross-validator class.

        """
        if isinstance(cv, int_t):
            if self.task.is_forecast:
                if cv == 1:
                    return SingleWindowSplitter(fh=range(1, len(self.og.test)))
                else:
                    return ExpandingWindowSplitter(
                        fh=range(1, len(self.og.test) + 1),
                        initial_window=(max_length - len(self.og.test)) // cv,
                        step_length=(max_length - len(self.og.test)) // cv,
                    )
            else:
                if cv == 1:
                    if self._config.metadata.get("groups") is not None:
                        return GroupShuffleSplit(
                            n_splits=cv,
                            test_size=self._config.test_size,
                            random_state=self.random_state,
                        )
                    elif self._config.stratify is None:
                        return ShuffleSplit(
                            n_splits=cv,
                            test_size=self._config.test_size,
                            random_state=self.random_state,
                        )
                    else:
                        return StratifiedShuffleSplit(
                            n_splits=cv,
                            test_size=self._config.test_size,
                            random_state=self.random_state,
                        )
                else:
                    rs = self.random_state if self._config.shuffle else None
                    if self._config.metadata.get("groups") is None:
                        if self._config.stratify is None:
                            return KFold(n_splits=cv)
                        else:
                            return StratifiedKFold(
                                n_splits=cv,
                                shuffle=self._config.shuffle,
                                random_state=rs,
                            )
                    else:
                        if self._config.stratify is None:
                            return GroupKFold(n_splits=cv)
                        else:
                            return StratifiedGroupKFold(
                                n_splits=cv,
                                shuffle=self._config.shuffle,
                                random_state=rs,
                            )
        else:
            return cv

    def _get_est(self, params: dict[str, Any]) -> Predictor:
        """Get the estimator instance.

        Use the multioutput meta-estimator if the estimator has
        no native support for multioutput.

        Use sktime's [make_reduction][] function for regressors
        in forecast tasks.

        Parameters
        ----------
        params: dict
            Hyperparameters for the estimator.

        Returns
        -------
        Predictor
            Estimator instance.

        """
        # Separate the params for the estimator from those in sub-estimators
        base_params, sub_params = {}, {}
        for name, value in params.items():
            if "__" not in name:
                base_params[name] = value
            else:
                sub_params[name] = value

        estimator = self._est_class(**base_params).set_params(**sub_params)

        fixed = tuple(params)
        if hasattr(self, "task"):
            if self.task.is_forecast and self._goal.name not in self._estimators:
                fixed = tuple(f"estimator__{f}" for f in fixed)

                # Forecasting task with a regressor
                if self.task.is_multioutput:
                    estimator = make_reduction(estimator, strategy="multioutput")
                else:
                    estimator = make_reduction(estimator, strategy="recursive")

            elif self.task is Task.multilabel_classification:
                if not self.native_multilabel:
                    fixed = tuple(f"base_estimator__{f}" for f in fixed)
                    estimator = ClassifierChain(estimator)

            elif self.task.is_multioutput and not self.native_multioutput:
                fixed = tuple(f"estimator__{f}" for f in fixed)
                if self.task.is_classification:
                    estimator = MultiOutputClassifier(estimator)
                elif self.task.is_regression:
                    estimator = MultiOutputRegressor(estimator)

        return self._inherit(estimator, fixed=fixed)

    def _fit_estimator(
        self,
        estimator: Predictor,
        data: tuple[pd.DataFrame, Pandas],
        validation: tuple[pd.DataFrame, Pandas] | None = None,
        trial: Trial | None = None,
    ) -> Predictor:
        """Fit the estimator and perform in-training validation.

        In-training evaluation is performed on models with the
        `partial_fit` method. After every partial fit, the estimator
        is evaluated (using only the main metric) on the validation
        data and, optionally, pruning is performed.

        Parameters
        ----------
        estimator: Predictor
            Instance to fit.

        data: tuple
            Training data of the form (X, y).

        validation: tuple or None
            Validation data of the form (X, y). If None, no validation
            is performed.

        trial: [Trial][] or None
            Active trial (during hyperparameter tuning).

        Returns
        -------
        Predictor
            Fitted instance.

        """
        kwargs: dict[str, Any] = {}
        if (sample_weight := self._config.get_sample_weight(data[0])) is not None:
            if "sample_weight" in sign(estimator.fit):
                kwargs["sample_weight"] = sample_weight
            if hasattr(estimator, "set_fit_request"):
                estimator.set_fit_request(sample_weight=True)
            if hasattr(estimator, "set_partial_fit_request"):
                estimator.set_partial_fit_request(sample_weight=True)

        if getattr(self, "validation", False) and hasattr(estimator, "partial_fit") and validation:
            # Loop over first parameter in estimator
            try:
                steps = estimator.get_params()[self.validation]
            except KeyError:
                # For meta-estimators like multioutput
                steps = estimator.get_params()[f"estimator__{self.validation}"]

            if self.task.is_classification:
                if self.task.is_multioutput:
                    if self.native_multilabel:
                        kwargs["classes"] = list(range(self.y.shape[1]))
                    else:
                        kwargs["classes"] = [np.unique(y) for y in get_cols(self.y)]
                else:
                    kwargs["classes"] = list(np.unique(self.y))

            for step in range(steps):
                estimator.partial_fit(*data, **self._est_params_fit, **kwargs)

                if not trial:
                    # Store train and validation scores on the main metric in evals attr
                    self._evals[f"{self._metric[0].name}_train"].append(
                        self._score_from_est(self._metric[0], estimator, *data)
                    )
                    self._evals[f"{self._metric[0].name}_test"].append(
                        self._score_from_est(self._metric[0], estimator, *validation)
                    )

                # Multi-objective optimization doesn't support pruning
                if trial and len(self._metric) == 1:
                    trial.report(
                        value=float(self._score_from_est(self._metric[0], estimator, *validation)),
                        step=step,
                    )

                    if trial.should_prune():
                        # Hacky solution to add the pruned step to the output
                        if self.validation in trial.params:
                            trial.params[self.validation] = f"{step}/{steps}"

                        trial.set_user_attr("estimator", estimator)
                        raise TrialPruned

        else:
            if isinstance(estimator, BaseForecaster):
                if estimator.get_tag("requires-fh-in-fit") and "fh" not in self._est_params_fit:
                    # Add the forecasting horizon to sktime estimators when required
                    kwargs["fh"] = self.test.index

                estimator.fit(data[1], X=check_empty(data[0]), **self._est_params_fit, **kwargs)
            else:
                estimator.fit(*data, **self._est_params_fit, **kwargs)

        return estimator

    def _best_score(self, metric: str | None = None) -> Scalar:
        """Return the best score for the model.

        The best score is the bootstrap or test score, checked in
        that order.

        Parameters
        ----------
        metric: str or None, default=None
            Name of the metric to use (for multi-metric runs). If None,
            the main metric is selected.

        Returns
        -------
        float
            Best score.

        """
        if self._bootstrap is None:
            return self.results[f"{metric or self._metric[0].name}_test"]
        else:
            return self.results[f"{metric or self._metric[0].name}_bootstrap"]

    def _final_output(self) -> str:
        """Return the model's final output as a string.

        If [bootstrapping][] was used, use the format: mean +- std.

        Returns
        -------
        str
            Final score representation.

        """
        try:
            if self._bootstrap is None:
                out = "   ".join(
                    [f"{met}: {rnd(self._best_score(met))}" for met in self._metric.keys()]
                )
            else:
                out = "   ".join(
                    [
                        f"{met}: {rnd(self.bootstrap[met].mean())} "
                        f"\u00B1 {rnd(self.bootstrap[met].std())}"
                        for met in self._metric.keys()
                    ]
                )

            if not self.task.is_forecast:
                # Annotate if model overfitted when train 20% > test on the main metric
                score_train = self.results[f"{self._metric[0].name}_train"]
                score_test = self.results[f"{self._metric[0].name}_test"]
                if (1.2 if score_train < 0 else 0.8) * score_train > score_test:
                    out += " ~"

        except (TypeError, AttributeError):  # Fails when errors="keep"
            out = "FAIL"

        return out

    @cache
    def _get_pred(
        self,
        rows: RowSelector,
        target: TargetSelector | None = None,
        method: PredictionMethods | Sequence[PredictionMethods] = "predict",
    ) -> tuple[Pandas, Pandas]:
        """Get the true and predicted values for a column.

        Predictions are made using the `decision_function` or
        `predict_proba` attributes whenever available, checked in
        that order.

        Parameters
        ----------
        rows: hashable, segment, sequence or dataframe
            [Selection of rows][row-and-column-selection] for which to
            get the predictions.

        target: str or None, default=None
            Target column to look at. Only for [multioutput tasks][].
            If None, all columns are returned.

        method: str or sequence, default="predict"
            Response method(s) used to get predictions. If sequence,
            the order provided states the order in which the methods
            are tried.

        Returns
        -------
        series or dataframe
            True values.

        series or dataframe
            Predicted values.

        """
        method_caller = _check_response_method(self.estimator, method).__name__

        X, y = self.branch._get_rows(rows, return_X_y=True)

        # Filter for indices in dataset (required for sh and ts)
        X = X.loc[X.index.isin(self._all.index)]
        y_true = y.loc[y.index.isin(self._all.index)]

        if self.task.is_forecast:
            try:
                if X.empty:
                    exog = None
                else:
                    # Statsmodels models such as SARIMAX and DF require all
                    # exogenous data after the last row of the train set
                    # Other models accept this format
                    Xe = pd.concat([self.test, self.holdout])
                    exog = Xe.loc[Xe.index <= X.index.max(), self.features]  # type: ignore[index]

                y_pred = self._prediction(
                    fh=X.index,
                    X=exog,
                    verbose=0,
                    method=method_caller,
                )

            except (ValueError, NotImplementedError) as ex:
                # Can fail for models that don't allow in-sample predictions
                self._log(
                    f"Failed to get predictions for model {self.name} "
                    f"on rows {rows}. Returning NaN. Exception: {ex}.", 3
                )
                y_pred = pd.Series([np.nan] * len(X), index=X.index)

        else:
            y_pred = self._prediction(X.index, verbose=0, method=method_caller)

        if self.task.is_multioutput:
            if target is not None:
                target = self.branch._get_target(target, only_columns=True)
                return y_true.loc[:, target], y_pred.loc[:, target]
        elif self.task.is_binary and y_pred.ndim > 1:
            return y_true, y_pred.iloc[:, 1]

        return y_true, y_pred

    def _score_from_est(
        self,
        scorer: Scorer,
        estimator: Predictor,
        X: pd.DataFrame,
        y: Pandas,
        sample_weight: Sequence[Scalar] | None = None,
    ) -> Float:
        """Calculate the metric score from an estimator.

        Parameters
        ----------
        scorer: Scorer
            Metric to calculate.

        estimator: Predictor
            Estimator instance to get the score from.

        X: pd.DataFrame
            Feature set.

        y: pd.Series or pd.DataFrame
            Target column(s) corresponding to `X`.

        sample_weight: sequence or None, default=None
            Sample weights for the `score` method.

        Returns
        -------
        float
            Calculated score.

        """
        if self.task.is_forecast:
            y_pred = estimator.predict(fh=y.index, X=check_empty(X))
        else:
            y_pred = to_tabular(
                data=_check_response_method(estimator, scorer._response_method)(X),
                index=y.index,
            )
            if isinstance(y_pred, pd.DataFrame) and self.task is Task.binary_classification:
                y_pred = y_pred.iloc[:, 1]  # Return probability of the positive class

        return self._score_from_pred(scorer, y, y_pred, sample_weight=sample_weight)

    def _score_from_pred(
        self,
        scorer: Scorer,
        y_true: Pandas,
        y_pred: Pandas,
        sample_weight: Sequence[Scalar] | None = None,
    ) -> Float:
        """Calculate the metric score from predicted values.

        Since sklearn metrics don't support multiclass-multioutput
        tasks, it calculates the mean of the scores over the target
        columns for such tasks.

        Parameters
        ----------
        scorer: Scorer
            Metric to calculate.

        y_true: pd.Series or pd.DataFrame
            True values in the target column(s).

        y_pred: pd.Series or pd.DataFrame
            Predicted values corresponding to y_true.

        sample_weight: sequence or None, default=None
            Sample weights for the `score` method. If not provided but available
            in the metadata, use those.

        Returns
        -------
        float
            Calculated score.

        """
        kwargs: dict[str, Any] = {}
        if "sample_weight" in sign(scorer._score_func):
            if sample_weight is not None:
                kwargs = {"sample_weight": sample_weight}
            elif (sw := self._config.get_sample_weight(y_true)) is not None:
                kwargs = {"sample_weight": sw}
                if hasattr(scorer, "set_score_request"):
                    scorer.set_score_request(sample_weight=True)

        func = lambda y1, y2: scorer._score_func(y1, y2, **scorer._kwargs, **kwargs)

        # Forecasting models can have NaN predictions, for example, when
        # using internally a boxcox transformation on negative predictions
        if self.task.is_forecast:
            y_pred = y_pred.dropna()
            y_true = y_true.loc[y_pred.index]

        if y_pred.empty:
            return np.nan

        if self.task is Task.multiclass_multioutput_classification:
            # Get the mean of the scores over the target columns
            return np.mean(
                [
                    scorer._sign * func(y_true[col1], y_pred[col2])
                    for col1, col2 in zip(y_true, y_pred, strict=True)
                ],
                axis=0,
            )
        else:
            return scorer._sign * func(y_true, y_pred)

    def _get_score(self, scorer: Scorer, rows: RowSelector) -> Scalar:
        """Calculate a metric score.

        Parameters
        ----------
        scorer: Scorer
            Metrics to calculate. If None, a selection of the most
            common metrics per task are used.

        rows: hashable, segment, sequence or dataframe
            [Selection of rows][row-and-column-selection] on which to
            calculate the metric.

        Returns
        -------
        int or float
            Metric score on the selected data set.

        """
        y_true, y_pred = self._get_pred(rows, method=scorer._response_method)
        result = rnd(self._score_from_pred(scorer, y_true, y_pred))
        # Log metric to mlflow run for predictions on data sets
        if self.experiment and isinstance(rows, str):
            MlflowClient().log_metric(
                run_id=self.run.info.run_id,
                key=f"{scorer.name}_{rows}",
                value=it(result),
            )

        return result

    @composed(crash, method_to_log, beartype)
    def hyperparameter_tuning(self, n_trials: Int, *, reset: Bool = False):
        """Run the hyperparameter tuning algorithm.

        Search for the best combination of hyperparameters. The function
        to optimize is evaluated either with a K-fold cross-validation
        on the training set or using a random train and validation split
        every trial. Use this method to continue the optimization.

        Parameters
        ----------
        n_trials: int
            Number of trials for the hyperparameter tuning.

        reset: bool, default=False
            Whether to start a new study or continue the existing one.

        """

        def objective(trial: Trial) -> list[float]:
            """Objective function for hyperparameter tuning.

            Parameters
            ----------
            trial: optuna.trial.Trial
               Model's hyperparameters used in this call of the BO.

            Returns
            -------
            list of float
                Scores of the estimator in this trial.

            """

            def fit_model(
                estimator: Predictor,
                train_idx: np.ndarray,
                val_idx: np.ndarray,
            ) -> tuple[Predictor, list[Float]]:
                """Fit the model. Function for parallelization.

                Divide the training set in a (sub) train and validation
                set for this fit. The sets are created from the original
                dataset to avoid data leakage since the training set is
                transformed using the pipeline fitted on the same set.
                Fit the model on custom_fit if exists, else normally.
                Return the score on the validation set.

                Parameters
                ----------
                estimator: Predictor
                    Model's estimator to fit.

                train_idx: np.array
                    Indices for the subtrain set.

                val_idx: np.array
                    Indices for the validation set.

                Returns
                -------
                Predictor
                    Fitted estimator.

                list of float
                    Scores of the estimator on the validation set.

                """
                X_sub = self.og.X_train.iloc[train_idx]
                y_sub = self.og.y_train.iloc[train_idx]
                X_val = self.og.X_train.iloc[val_idx]
                y_val = self.og.y_train.iloc[val_idx]

                # Transform subsets if there is a pipeline
                if len(pl := clone(self.pipeline)) > 0:
                    X_sub, y_sub = pl.fit_transform(X_sub, y_sub)
                    X_val, y_val = pl.transform(X_val, y_val)

                estimator = self._fit_estimator(
                    estimator=estimator,
                    data=(X_sub, y_sub),
                    validation=(X_val, y_val),
                    trial=trial,
                )

                scores = [
                    self._score_from_est(metric, estimator, X_val, y_val)
                    for metric in self._metric
                ]

                return estimator, scores

            # Start trial ========================================== >>

            params = self._get_parameters(trial)

            # Since the suggested values are not the exact same values used
            # in the estimator (rounded by _get_parameters), we implement
            # this hacky method to overwrite the params in storage
            if isinstance(self.study._storage, InMemoryStorage):
                trial._cached_frozen_trial.params = params
                frozen_trial = self.study._storage._get_trial(trial.number)
                frozen_trial.params = params
                self.study._storage._set_trial(trial.number, frozen_trial)

            # Store user defined tags
            for key, value in self._ht["tags"].items():
                trial.set_user_attr(key, value)

            # Create estimator instance with trial-specific hyperparameters
            estimator = self._get_est(self._est_params | self._trial_to_est(params))

            # Check if the same parameters have already been evaluated
            for t in trial.study.get_trials(deepcopy=False, states=(TrialState.COMPLETE,))[::-1]:
                if trial.params == t.params:
                    # Get same estimator and score as previous evaluation
                    estimator = deepcopy(t.user_attrs["estimator"])
                    score = t.value if len(self._metric) == 1 else t.values
                    break
            else:
                splitter = self._get_cv(self._ht["cv"], max_length=len(self.og.train))

                # Follow the same splitting strategy as atom
                stratify = self._config.get_stratify_column(self.og.train)
                groups = self._config.get_metadata(self.og.train).get("groups")

                kwargs: dict[str, Any] = {next(iter(sign(splitter.split))): self.og.X_train}
                if stratify is not None:
                    kwargs["y"] = stratify
                if groups is not None:
                    kwargs["groups"] = groups

                # Parallel loop over fit_model
                results = Parallel(n_jobs=self.n_jobs)(
                    delayed(fit_model)(estimator, i, j) for i, j in splitter.split(**kwargs)
                )

                estimator = results[0][0]
                score = np.mean(scores := [r[1] for r in results], axis=0).tolist()

                if len(results) > 1:
                    # Report cv scores for termination judgment
                    report_cross_validation_scores(trial, scores)

            trial.set_user_attr("estimator", estimator)

            return score

        # Running hyperparameter tuning ============================ >>

        self._log(f"Running hyperparameter tuning for {self.fullname}...", 1)

        # Check the validity of the provided parameters
        self._check_est_params()

        # Assign custom distributions or use predefined
        dist = self._get_distributions() if hasattr(self, "_get_distributions") else {}
        if self._ht.get("distributions"):
            # Select default distributions
            inc, exc = [], []
            for name in [k for k, v in self._ht["distributions"].items() if v is None]:
                # If it's a name, use the predefined dimension
                if name.startswith("!"):
                    exc.append(n := name[1:])
                else:
                    inc.append(n := name)

                if n not in dist:
                    raise ValueError(
                        "Invalid value for the distributions parameter. "
                        f"Parameter {n} is not a predefined hyperparameter "
                        f"of the {self.fullname} model. See the model's "
                        "documentation for an overview of the available "
                        "hyperparameters and their distributions."
                    )

            if inc and exc:
                raise ValueError(
                    "Invalid value for the distributions parameter. You can either "
                    "include or exclude hyperparameters, not combinations of these."
                )
            elif exc:
                # If distributions were excluded with `!`, select all but those
                self._ht["distributions"] = {k: v for k, v in dist.items() if k not in exc}
            elif inc:
                self._ht["distributions"] = {k: v for k, v in dist.items() if k in inc}
        else:
            self._ht["distributions"] = dist

        # Drop hyperparameter if already defined in est_params
        self._ht["distributions"] = {
            k: v for k, v in self._ht["distributions"].items() if k not in self._est_params
        }

        # If no hyperparameters to optimize, skip ht
        if not self._ht["distributions"]:
            self._log(" --> Skipping study. No hyperparameters to optimize.", 2)
            return

        if not self._study or reset:
            kw: dict[str, Any] = {k: v for k, v in self._ht.items() if k in sign(create_study)}

            if len(self._metric) == 1:
                kw["direction"] = "maximize"
                kw["sampler"] = kw.pop("sampler", TPESampler(seed=self.random_state))
            else:
                kw["directions"] = ["maximize"] * len(self._metric)
                kw["sampler"] = kw.pop("sampler", NSGAIISampler(seed=self.random_state))

            self._study = create_study(study_name=self.name, **kw)

        kw = {k: v for k, v in self._ht.items() if k in sign(Study.optimize)}
        n_jobs = kw.pop("n_jobs", 1)

        # Initialize live study plot
        if self._ht.get("plot", False) and n_jobs == 1:
            plot_callback = PlotCallback(
                name=self.fullname,
                metric=self._metric.keys(),
                aesthetics=self.aesthetics,
            )
        else:
            plot_callback = None

        callbacks = [*kw.pop("callbacks", []), TrialsCallback(self, n_jobs)]
        callbacks += [plot_callback] if plot_callback else []

        self._study.optimize(
            func=objective,
            n_trials=int(n_trials),
            n_jobs=n_jobs,
            callbacks=callbacks,
            show_progress_bar=kw.pop("show_progress_bar", self.verbose == 1),
            **kw,
        )

        if len(self.study.get_trials(states=[TrialState.COMPLETE])) == 0:
            self._study = None
            self._log(
                "The study didn't complete any trial successfully. "
                "Skipping hyperparameter tuning.",
                1,
                severity="warning",
            )
            return

        self._log(f"Hyperparameter tuning {'-' * 27}", 1)
        self._log(f"Best trial --> {self.best_trial.number}", 1)
        self._log("Best parameters:", 1)
        self._log("\n".join([f" --> {k}: {v}" for k, v in self.best_params.items()]), 1)
        out = [
            f"{met}: {rnd(self.trials.loc[self.best_trial.number, met])}"
            for met in self._metric.keys()
        ]
        self._log(f"Best evaluation --> {'   '.join(out)}", 1)
        self._log(f"Time elapsed: {time_to_str(self.trials.iat[-1, -2])}", 1)

    @composed(crash, method_to_log, beartype)
    def fit(self, X: pd.DataFrame | None = None, y: Pandas | None = None, *, prefit: bool = False):
        """Fit and validate the model.

        The estimator is fitted using the best hyperparameters found
        during hyperparameter tuning. Afterwards, the estimator is
        evaluated on the test set. Only use this method to re-fit the
        model after having continued the study.

        Parameters
        ----------
        X: pd.DataFrame or None
            Feature set with shape=(n_samples, n_features). If None,
            `self.X_train` is used.

        y: pd.Series, pd.DataFrame or None
            Target column(s) corresponding to `X`. If None, `self.y_train`
            is used.

        prefit: bool, default=False
            Whether the estimator is already fitted. If True, only evaluate
            the model.

        """
        t_init = dt.now()

        if X is None:
            X = self.X_train
        if y is None:
            y = self.y_train

        self.clear()  # Reset model's state

        if self._study is None:
            self._log(f"Results for {self.fullname}:", 1)
        self._log(f"Fit {'-' * 45}", 1)

        # Assign estimator if not done already
        if self._estimator is None:
            self._check_est_params()
            self._estimator = self._get_est(self._est_params | self.best_params)

        if not prefit:
            self._estimator = self._fit_estimator(
                estimator=self.estimator,
                data=(X, y),
                validation=(self.X_test, self.y_test),
            )

        for ds in ("train", "test"):
            out = [f"{met.name}: {self._get_score(met, ds)}" for met in self._metric]
            self._log(f"T{ds[1:]} evaluation --> {'   '.join(out)}", 1)

        # Get duration and print to log
        self._time_fit += (dt.now() - t_init).total_seconds()
        self._log(f"Time elapsed: {time_to_str(self._time_fit)}", 1)

        # Track results in mlflow ================================== >>

        # Log parameters, metrics, model and data to mlflow
        if self.experiment:
            with mlflow.start_run(run_id=self.run.info.run_id):
                mlflow.set_tags(
                    {
                        "name": self.name,
                        "model": self.fullname,
                        "branch": self.branch.name,
                        **self._ht["tags"],
                    }
                )

                # Mlflow only accepts params with char length <250
                mlflow.log_params(
                    {k: v for k, v in self.estimator.get_params().items() if len(str(v)) <= 250}
                )

                # Save evals for models with in-training validation
                if self.evals:
                    for key, value in self.evals.items():
                        for step in range(len(value)):
                            mlflow.log_metric(f"evals_{key}", value[step], step=step)

                # The rest of the metrics are tracked when calling _get_score
                mlflow.log_metric("time_fit", self._time_fit)

                mlflow.sklearn.log_model(
                    sk_model=self.estimator,
                    artifact_path=self._est_class.__name__,
                    signature=infer_signature(
                        model_input=self.X,
                        model_output=self.estimator.predict(self.X_test.iloc[[0]]),
                    ),
                    input_example=self.X.iloc[[0]],
                )

                if self.log_data:
                    for ds in ("train", "test"):
                        mlflow.log_input(dataset=from_pandas(getattr(self, ds)), context=ds)

                if self.log_pipeline:
                    mlflow.sklearn.log_model(
                        sk_model=self.export_pipeline(),
                        artifact_path=f"{self._est_class.__name__}_pipeline",
                        signature=infer_signature(
                            model_input=self.X,
                            model_output=self.estimator.predict(self.X_test.iloc[[0]]),
                        ),
                        input_example=self.X.iloc[[0]],
                    )

    @composed(crash, method_to_log, beartype)
    def bootstrapping(self, n_bootstrap: Int, *, reset: Bool = False):
        """Apply a bootstrap algorithm.

        Take bootstrapped samples from the training set and test them
        on the test set to get a distribution of the model's results.

        Parameters
        ----------
        n_bootstrap: int
           Number of bootstrapped samples to fit on.

        reset: bool, default=False
            Whether to start a new run or continue the existing one.

        """
        t_init = dt.now()

        if self._bootstrap is None or reset:
            self._bootstrap = pd.DataFrame(columns=self._metric.keys())
            self._bootstrap.index.name = "sample"
            self._time_bootstrap = 0

        for i in range(n_bootstrap):
            # Create stratified samples with replacement
            sample_x, sample_y = resample(
                self.X_train,
                self.y_train,
                replace=True,
                random_state=i + (self.random_state or 0),
                stratify=self.y_train,
            )

            # Fit on a bootstrapped set
            estimator = self._fit_estimator(self.estimator, data=(sample_x, sample_y))

            # Get scores on the test set
            scores = pd.DataFrame(
                {
                    m.name: [self._score_from_est(m, estimator, self.X_test, self.y_test)]
                    for m in self._metric
                }
            )

            self._bootstrap = pd.concat([self._bootstrap, scores], ignore_index=True)

        self._log(f"Bootstrap {'-' * 39}", 1)
        out = [
            f"{m.name}: {rnd(self.bootstrap.mean()[i])} \u00B1 {rnd(self.bootstrap.std()[i])}"
            for i, m in enumerate(self._metric)
        ]
        self._log(f"Evaluation --> {'   '.join(out)}", 1)

        self._time_bootstrap += (dt.now() - t_init).total_seconds()
        self._log(f"Time elapsed: {time_to_str(self._time_bootstrap)}", 1)

    # Utility properties =========================================== >>

    @property
    def name(self) -> str:
        """Name of the model.

        Use the property's `@setter` to change the model's name. The
        acronym always stays at the beginning of the model's name. If
        the model is being tracked by [mlflow][tracking], the name of
        the corresponding run also changes.

        """
        return self._name

    @name.setter
    @beartype
    def name(self, value: str):
        """Change the model's name."""
        # Drop the acronym if provided by the user
        if re.match(f"{self.acronym}_", value, re.I):
            value = value[len(self.acronym) + 1:]

        # Add the acronym in front (with right capitalization)
        self._name = f"{self.acronym}{f'_{value}' if value else ''}"

        if self.experiment:  # Change name in mlflow's run
            MlflowClient().set_tag(self.run.info.run_id, "mlflow.runName", self.name)

        self._log(f"Model {self.name} successfully renamed to {self._name}.", 1)

    @cached_property
    def task(self) -> Task:
        """Dataset's [task][] type."""
        return self._goal.infer_task(self.y)

    @property
    def og(self) -> Branch:
        """Branch containing the original dataset.

        This branch contains the data prior to any transformations.
        It redirects to the current branch if its pipeline is empty
        to not have the same data in memory twice.

        """
        return self._og

    @property
    def branch(self) -> Branch:
        """Current active branch."""
        return self._branch

    @property
    def run(self) -> Run:
        """Mlflow run corresponding to this model.

        This property is only available for models that with mlflow
        [tracking][] enabled.

        """
        if self.experiment:
            return self._run

        raise AttributeError("This model has no mlflow experiment.")

    @property
    def study(self) -> Study:
        """Optuna study used for hyperparameter tuning.

        This property is only available for models that ran
        [hyperparameter tuning][].

        """
        if self._study is not None:
            return self._study

        raise AttributeError("This model didn't run hyperparameter tuning.")

    @property
    def trials(self) -> pd.DataFrame:
        """Overview of the trials' results.

        This property is only available for models that ran
        [hyperparameter tuning][]. All durations are in seconds.
        Columns include:

        - **[param_name]:** Parameter value used in this trial.
        - **estimator:** Estimator used in this trial.
        - **[metric_name]:** Metric score of the trial.
        - **[best_metric_name]:** Best score so far in this study.
        - **time_trial:** Duration of the trial.
        - **time_ht:** Duration of the hyperparameter tuning.
        - **state:** Trial's state (COMPLETE, PRUNED, FAIL).

        """
        if self._study is not None:
            data: dict[str, list[Any]] = defaultdict(list)
            for t in self._study.trials:
                data["trial"].append(t.number)
                for p in t.params:
                    data[p].append(t.params[p])
                data["estimator"].append(t.user_attrs.get("estimator"))
                for i, met in enumerate(self._metric.keys()):
                    if len(self._metric) == 1:
                        data[met].append(t.value or np.nan)
                    else:
                        data[met].append(t.values[i] if t.values else np.nan)
                    data[f"best_{met}"] = np.nanmax(data[met])
                if t.datetime_complete and t.datetime_start:
                    data["time_trial"].append(
                        (t.datetime_complete - t.datetime_start).total_seconds()
                    )
                data["time_ht"].append(np.sum(data["time_trial"]))
                data["state"].append(t.state.name)

            return pd.DataFrame(data).set_index("trial")

        raise AttributeError("The model didn't run hyperparameter tuning.")

    @property
    def best_trial(self) -> FrozenTrial:
        """Trial that returned the highest score.

        For [multi-metric runs][], the best trial is the trial that
        performed best on the main metric. Use the property's `@setter`
        to change the best trial. See [here][example-hyperparameter-tuning]
        an example. This property is only available for models that
        ran [hyperparameter tuning][].

        """
        if self._study is not None:
            if self._best_trial:
                return self._best_trial
            elif len(self._metric) == 1:
                return self.study.best_trial
            else:
                # Sort trials by the best score on the main metric
                return sorted(self.study.best_trials, key=lambda x: x.values[0])[0]

        raise AttributeError("The model didn't run hyperparameter tuning.")

    @best_trial.setter
    @beartype
    def best_trial(self, value: IntLargerEqualZero | None):
        """Assign the study's best trial.

        The hyperparameters selected in this trial are used to train
        the estimator. This property is only available for models that
        ran [hyperparameter tuning][].

        """
        if value is None:
            self._best_trial = None  # Reset best trial selection
        elif value not in self.trials.index:
            raise ValueError(
                "Invalid value for the best_trial. The "
                f"value should be a trial number, got {value}."
            )
        else:
            self._best_trial = self.study.trials[value]

    @property
    def best_params(self) -> dict[str, Any]:
        """Estimator's parameters in the [best trial][self-best_trial].

        This property is only available for models that ran
        [hyperparameter tuning][].

        """
        if self._study is not None:
            return dict(self._trial_to_est(self.best_trial.params))
        else:
            return {}

    @property
    def estimator(self) -> Predictor:
        """Estimator fitted on the training set."""
        if self._estimator is not None:
            return self._estimator

        raise AttributeError("This model hasn't been fitted yet.")

    @property
    def evals(self) -> dict[str, list[Float]]:
        """Scores obtained per iteration of the training.

        Only the scores of the [main metric][metric] are tracked.
        Included keys are: train and test. This property is only
        available for models with [in-training-validation][].

        """
        return self._evals

    @property
    def bootstrap(self) -> pd.DataFrame:
        """Overview of the bootstrapping scores.

        The dataframe has shape=(n_bootstrap, metric) and shows the
        score obtained by every bootstrapped sample for every metric.
        Using `atom.bootstrap.mean()` yields the same values as
        `[metric]_bootstrap`. This property is only available for
        models that ran [bootstrapping][].

        """
        if self._bootstrap is not None:
            return self._bootstrap

        raise AttributeError("This model didn't run bootstrapping.")

    @property
    def results(self) -> pd.Series:
        """Overview of the model results.

        All durations are in seconds. Possible values include:

        - **[metric]_ht:** Score obtained by the hyperparameter tuning.
        - **time_ht:** Duration of the hyperparameter tuning.
        - **[metric]_train:** Metric score on the train set.
        - **[metric]_test:** Metric score on the test set.
        - **time_fit:** Duration of the model fitting on the train set.
        - **[metric]_bootstrap:** Mean score on the bootstrapped samples.
        - **time_bootstrap:** Duration of the bootstrapping.
        - **time:** Total duration of the run.

        """
        data = {}
        if self._study is not None:
            for met in self._metric.keys():
                data[f"{met}_ht"] = self.trials.loc[self.best_trial.number, met]
            data["time_ht"] = self.trials.iloc[-1, -2]
        for met in self._metric:
            for ds in ["train", "test"] + ([] if self.holdout is None else ["holdout"]):
                data[f"{met.name}_{ds}"] = self._get_score(met, ds)
        data["time_fit"] = self._time_fit
        if self._bootstrap is not None:
            for met in self._metric.keys():
                data[f"{met}_bootstrap"] = self.bootstrap[met].mean()
            data["time_bootstrap"] = self._time_bootstrap
        data["time"] = data.get("time_ht", 0) + self._time_fit + self._time_bootstrap
        return pd.Series(data, name=self.name)

    @property
    def feature_importance(self) -> pd.Series:
        """Normalized feature importance scores.

        The sum of importances for all features is 1. The scores are
        extracted from the estimator's `scores_`, `coef_` or
        `feature_importances_` attribute, checked in that order.
        This property is only available for estimators with at least
        one of those attributes.

        """
        data: np.ndarray | None = None

        for attr in ("scores_", "coef_", "feature_importances_"):
            if hasattr(self.estimator, attr):
                data = getattr(self.estimator, attr)

        # Get the mean value for meta-estimators
        if data is None and hasattr(self.estimator, "estimators_"):
            estimators = self.estimator.estimators_
            if all(hasattr(x, "feature_importances_") for x in estimators):
                data_l = [fi.feature_importances_ for fi in estimators]
            elif all(hasattr(x, "coef_") for x in estimators):
                data_l = [
                    np.linalg.norm(fi.coef_, axis=np.argmin(fi.coef_.shape), ord=1)
                    for fi in estimators
                ]
            else:
                # For ensembles that mix attributes
                raise ValueError(
                    "Failed to calculate the feature importance for meta-estimator "
                    f"{self._est_class.__name__}. The underlying estimators have a "
                    "mix of feature_importances_ and coef_ attributes."
                )

            # Trim each coef to the number of features in the 1st estimator
            # ClassifierChain adds features to subsequent estimators
            min_length = np.min([len(c) for c in data_l])
            data = np.mean([c[:min_length] for c in data_l], axis=0)

        if data is not None:
            return pd.Series(
                data=(data_c := np.abs(data.flatten())) / data_c.sum(),
                index=self.features,
                name="feature_importance",
                dtype=float,
            ).sort_values(ascending=False)
        else:
            raise AttributeError(
                "Failed to calculate the feature importance for estimator "
                f"{self._est_class.__name__}. The estimator doesn't have the"
                f"scores_, coef_ nor feature_importances_ attribute."
            )

    # Data Properties ============================================== >>

    @property
    def pipeline(self) -> Pipeline:
        """Pipeline of transformers.

        Models that used [automated feature scaling][] have the scaler
        added.

        !!! tip
            Use the [plot_pipeline][] method to visualize the pipeline.

        """
        if self.scaler:
            return Pipeline(
                steps=[*self.branch.pipeline.steps, ("AutomatedScaler", self.scaler)],
                memory=self.memory,
            )
        else:
            return self.branch.pipeline

    @property
    def dataset(self) -> pd.DataFrame:
        """Complete data set."""
        return merge(self.X, self.y)

    @property
    def train(self) -> pd.DataFrame:
        """Training set."""
        return merge(self.X_train, self.y_train)

    @property
    def test(self) -> pd.DataFrame:
        """Test set."""
        return merge(self.X_test, self.y_test)

    @property
    def holdout(self) -> pd.DataFrame | None:
        """Holdout set."""
        if (holdout := self.branch.holdout) is not None:
            if self.scaler:
                return merge(self.scaler.transform(holdout[self.features]), holdout[self.target])
            else:
                return holdout
        else:
            return None

    @property
    def X(self) -> pd.DataFrame:
        """Feature set."""
        return pd.concat([self.X_train, self.X_test])

    @property
    def y(self) -> Pandas:
        """Target column(s)."""
        return pd.concat([self.y_train, self.y_test])

    @property
    def X_train(self) -> pd.DataFrame:
        """Features of the training set."""
        exclude = self.branch.features.isin(self._config.ignore)
        X_train = self.branch.X_train.iloc[-self._train_idx:, ~exclude]
        if self.scaler:
            return cast(pd.DataFrame, self.scaler.transform(X_train))
        else:
            return X_train

    @property
    def y_train(self) -> Pandas:
        """Target column of the training set."""
        return self.branch.y_train[-self._train_idx:]

    @property
    def X_test(self) -> pd.DataFrame:
        """Features of the test set."""
        exclude = self.branch.features.isin(self._config.ignore)
        X_test = self.branch.X_test.iloc[:, ~exclude]
        if self.scaler:
            return cast(pd.DataFrame, self.scaler.transform(X_test))
        else:
            return X_test

    @property
    def X_holdout(self) -> pd.DataFrame | None:
        """Features of the holdout set."""
        if self.holdout is not None:
            return self.holdout[self.features]
        else:
            return None

    @property
    def y_holdout(self) -> Pandas | None:
        """Target column of the holdout set."""
        if self.holdout is not None:
            return self.holdout[self.branch.target]
        else:
            return None

    @property
    def shape(self) -> tuple[Int, Int]:
        """Shape of the dataset (n_rows, n_columns)."""
        return self.dataset.shape

    @property
    def columns(self) -> pd.Index:
        """Name of all the columns."""
        return self.dataset.columns

    @property
    def n_columns(self) -> int:
        """Number of columns."""
        return len(self.columns)

    @property
    def features(self) -> pd.Index:
        """Name of the features."""
        return self.columns[:-self.branch._data.n_targets]

    @property
    def n_features(self) -> int:
        """Number of features."""
        return len(self.features)

    @property
    def _all(self) -> pd.DataFrame:
        """Dataset + holdout.

        Note that calling this property triggers the holdout set
        calculation.

        """
        return pd.concat([self.dataset, self.holdout])

    # Utility methods ============================================== >>

    @available_if(has_task("classification"))
    @composed(crash, method_to_log)
    def calibrate(
        self,
        method: Literal["sigmoid", "isotonic"] = "sigmoid",
        *,
        train_on_test: bool = False,
    ):
        """Calibrate and retrain the model.

        Uses sklearn's [CalibratedClassifierCV][] to apply probability
        calibration on the model. The new classifier replaces the
        `estimator` attribute. If there is an active mlflow experiment,
        a new run is started using the name `[model_name]_calibrate`.
        Since the estimator changed, the model is [cleared][self-clear].
        Only for classifiers.

        !!! note
            By default, the calibration is optimized using the training
            set (which is already used for the initial training). This
            approach is subject to undesired overfitting. It's preferred
            to use `train_on_test=True`, which uses the test set for
            calibration, but only if there is another, independent set
            for testing ([holdout set][data-sets]).

        Parameters
        ----------
        method: str, default="sigmoid"
            The method to use for calibration. Choose from:

            - "sigmoid": Corresponds to [Platt's method][plattsmethod]
              (i.e., a logistic regression model).
            - "isotonic": Non-parametric approach. It's not advised
              to use this calibration method with too few samples (<1000)
              since it tends to overfit.

        train_on_test: bool, default=False
            Whether to train the calibrator on the test set.

        """
        self._estimator = CalibratedClassifierCV(
            estimator=self.estimator,
            method=method,
            cv="prefit",
            n_jobs=self.n_jobs,
        )

        # Assign a mlflow run to the new estimator
        if self.experiment:
            self._run = mlflow.start_run(run_name=f"{self.name}_calibrate")
            mlflow.end_run()

        if not train_on_test:
            self.fit(self.X_train, self.y_train)
        else:
            self.fit(self.X_test, self.y_test)

    @composed(crash, method_to_log)
    def clear(self):
        """Reset attributes and clear cache from the model.

        Reset certain model attributes to their initial state, deleting
        potentially large data arrays. Use this method to free some
        memory before [saving][atomclassifier-save] the instance. The
        affected attributes are:

        - [In-training validation][] scores
        - [Cached predictions][predicting].
        - [Shap values][shap]
        - [App instance][self-create_app]
        - [Dashboard instance][self-create_dashboard]
        - Calculated [holdout data sets][data-sets]

        """
        self._evals = defaultdict(list)
        self._get_pred.clear_cache()
        self._shap_explanation = None
        self.__dict__.pop("app", None)
        self.__dict__.pop("dashboard", None)
        self.branch.__dict__.pop("holdout", None)

    @composed(crash, method_to_log)
    def create_app(self, **kwargs):
        """Create an interactive app to test model predictions.

        Demo your machine learning model with a friendly web interface.
        This app launches directly in the notebook or on an external
        browser page. The created [Interface][] instance can be accessed
        through the `app` attribute.

        Parameters
        ----------
        **kwargs
            Additional keyword arguments for the [Interface][] instance
            or the [Interface.launch][launch] method.

        """

        def inference(*X) -> Scalar | str | list[Scalar | str]:
            """Apply inference on the row provided by the app.

            Parameters
            ----------
            *X
                Features provided by the user in the app.

            Returns
            -------
            int, float, str or list
                Original label or list of labels for multioutput tasks.

            """
            conv = lambda elem: elem.item() if hasattr(elem, "item") else elem

            with adjust(self, transform="pandas"):
                y_pred = self.predict([X])

            if isinstance(y_pred, pd.DataFrame):
                return [conv(elem) for elem in y_pred.iloc[0, :]]
            else:
                return conv(y_pred[0])

        check_dependency("gradio")
        from gradio import Interface
        from gradio.components import Dropdown, Textbox

        self._log("Launching app...", 1)

        inputs = []
        for name, column in self.og.X.items():
            if column.dtype.kind in "ifu":
                inputs.append(Textbox(label=name))
            else:
                inputs.append(Dropdown(list(column.unique()), label=name))

        self.app = Interface(
            fn=inference,
            inputs=inputs,
            outputs=["label"] * self.branch._data.n_targets,
            allow_flagging=kwargs.pop("allow_flagging", "never"),
            **{k: v for k, v in kwargs.items() if k in sign(Interface)},
        )

        self.app.launch(**{k: v for k, v in kwargs.items() if k in sign(Interface.launch)})

    @available_if(has_task("!multioutput"))
    @composed(crash, method_to_log, beartype)
    def create_dashboard(
        self,
        rows: RowSelector = "test",
        *,
        filename: str | Path | None = None,
        **kwargs,
    ):
        """Create an interactive dashboard to analyze the model.

        ATOM uses the [explainerdashboard][explainerdashboard_package]
        package to provide a quick and easy way to analyze and explain
        the predictions and workings of the model. The dashboard allows
        you to investigate SHAP values, permutation importances,
        interaction effects, partial dependence plots, all kinds of
        performance plots, and even individual decision trees.

        By default, the dashboard renders in a new tab in your default
        browser, but if preferable, you can render it inside the
        notebook using the `mode="inline"` parameter. The created
        [ExplainerDashboard][] instance can be accessed through the
        `dashboard` attribute. This method is not available for
        [multioutput tasks][].

        !!! note
            Plots displayed by the dashboard are not created by ATOM and
            can differ from those retrieved through this package.

        Parameters
        ----------
        rows: hashable, segment, sequence or dataframe, default="test"
            [Selection of rows][row-and-column-selection] to get the
            report from.

        filename: str, Path or None, default=None
            Filename or [pathlib.Path][] of the file to save. None to not
            save anything.

        **kwargs
            Additional keyword arguments for the [ExplainerDashboard][]
            instance.

        """
        check_dependency("explainerdashboard")
        from explainerdashboard import (
            ClassifierExplainer, ExplainerDashboard, RegressionExplainer,
        )

        self._log("Creating dashboard...", 1)

        Xt, yt = self.branch._get_rows(rows, return_X_y=True)

        if self.scaler:
            Xt = cast(pd.DataFrame, self.scaler.transform(Xt))

        # Get shap values from the internal ShapExplanation object
        exp = self._shap.get_explanation(Xt, target=(0,))

        # Explainerdashboard requires all the target classes
        if self.task.is_classification:
            if self.task.is_binary:
                if exp.values.shape[-1] != 2:
                    exp.base_values = [np.array(1 - exp.base_values), exp.base_values]
                    exp.values = [np.array(1 - exp.values), exp.values]
            else:
                # Explainer expects a list of np.array with shap values for each class
                exp.values = list(np.moveaxis(exp.values, -1, 0))

        params = {"permutation_metric": self._metric, "n_jobs": self.n_jobs}
        if self.task.is_classification:
            explainer = ClassifierExplainer(self.estimator, Xt, yt, **params)
        else:
            explainer = RegressionExplainer(self.estimator, Xt, yt, **params)

        explainer.set_shap_values(exp.base_values, exp.values)

        self.dashboard = ExplainerDashboard(
            explainer=explainer,
            mode=kwargs.pop("mode", "external"),
            **kwargs,
        )
        self.dashboard.run()

        if filename:
            if (path := Path(filename)).suffix != ".html":
                path = path.with_suffix(".html")

            self.dashboard.save_html(path)
            self._log("Dashboard successfully saved.", 1)

    @composed(crash, method_to_log)
    def cross_validate(self, *, include_holdout: Bool = False, **kwargs) -> Styler:
        """Evaluate the model using cross-validation.

        This method cross-validates the whole pipeline on the complete
        dataset. Use it to assess the robustness of the model's
        performance. If the scoring method is not specified in `kwargs`,
        it uses atom's metric. The results of the cross-validation are
        stored in the model's `cv` attribute.

        !!! tip
            This method returns a pandas' [Styler][] object. Convert
            the result back to a regular dataframe using its `data`
            attribute.

        Parameters
        ----------
        include_holdout: bool, default=False
            Whether to include the holdout set (if available) in the
            cross-validation.

        **kwargs
            Additional keyword arguments for one of these functions.

            - For forecast tasks: [evaluate][sktimeevaluate].
            - Else: [cross_validate][sklearncrossvalidate].

        Returns
        -------
        [Styler][]
            Overview of the results.

        """
        self._log("Applying cross-validation...", 1)

        if not include_holdout:
            X = self.og.X
            y = self.og.y
        else:
            X = self.og._all[self.og.features]
            y = self.og._all[self.og.target]

        # Assign scoring from atom if not specified
        if kwargs.get("scoring"):
            scorer = get_custom_scorer(kwargs.pop("scoring"), pos_label=self._config.pos_label)
            scoring = {scorer.name: scorer}
        else:
            scoring = dict(self._metric)

        if self.task.is_forecast:
            self.cv = evaluate(
                forecaster=self.export_pipeline(),
                y=y,
                X=X,
                scoring=[
                    make_forecasting_scorer(
                        func=metric._score_func,
                        name=name,
                        greater_is_better=metric._sign == 1,
                    )
                    for name, metric in scoring.items()
                ],
                cv=self._get_cv(kwargs.pop("cv", 5), max_length=len(X)),
                backend=kwargs.pop("backend", self.backend if self.backend != "ray" else None),
                backend_params=kwargs.pop("backend_params", {"n_jobs": self.n_jobs}),
                return_data=True,  # Required for plot_cv_splits
            )
        else:
            if "groups" in kwargs:
                raise ValueError(
                    "The parameter groups can not be passed directly to cross_validate. "
                    "ATOM uses metadata routing to manage data groups. Pass the groups to "
                    "atom's 'metadata' parameter in the constructor."
                )

            # Monkey patch sklearn's _fit_and_score function to allow
            # for pipelines that drop samples during transformation
            with patch("sklearn.model_selection._validation._fit_and_score", fit_and_score):
                self.cv = cross_validate(
                    estimator=self.export_pipeline(),
                    X=X,
                    y=y,
                    scoring=scoring,
                    cv=self._get_cv(kwargs.pop("cv", 5), max_length=len(X)),
                    params=self._config.get_metadata(X),
                    return_train_score=kwargs.pop("return_train_score", True),
                    error_score=kwargs.pop("error_score", "raise"),
                    n_jobs=kwargs.pop("n_jobs", self.n_jobs),
                    return_indices=True,  # Required for plot_cv_splits
                    **kwargs,
                )

        df = pd.DataFrame()
        for m in scoring:
            if f"train_{m}" in self.cv:
                df[f"train_{m}"] = self.cv[f"train_{m}"]
            if f"test_{m}" in self.cv:
                df[f"test_{m}"] = self.cv[f"test_{m}"]
        df["time"] = self.cv["fit_time"]
        df.loc["mean"] = df.mean()

        return (
            df
            .style
            .highlight_max(props=COLOR_SCHEME, subset=[c for c in df if not c.startswith("time")])
            .highlight_min(props=COLOR_SCHEME, subset=[c for c in df if c.startswith("time")])
        )

    @composed(crash, beartype)
    def evaluate(self, metric: MetricConstructor = None, rows: RowSelector = "test") -> pd.Series:
        """Get the model's scores for the provided metrics.

        !!! tip
            Use the [get_best_threshold][self-get_best_threshold] or
            [plot_threshold][] method to determine a suitable threshold
            for a binary classifier.

        Parameters
        ----------
        metric: str, func, scorer, sequence or None, default=None
            Metrics to calculate. If None, a selection of the most
            common metrics per task is used.

        rows: hashable, segment, sequence or dataframe, default="test"
            [Selection of rows][row-and-column-selection] to calculate
            metric on.

        Returns
        -------
        pd.Series
            Scores of the model.

        """
        # Predefined metrics to show
        if metric is None:
            if self.task.is_classification:
                if self.task is Task.binary_classification:
                    metric = [
                        "accuracy",
                        "ap",
                        "ba",
                        "f1",
                        "jaccard",
                        "mcc",
                        "precision",
                        "recall",
                        "auc",
                    ]
                elif self.task.is_multiclass:
                    metric = [
                        "ba",
                        "f1_weighted",
                        "jaccard_weighted",
                        "mcc",
                        "precision_weighted",
                        "recall_weighted",
                    ]
                elif self.task is Task.multilabel_classification:
                    metric = [
                        "accuracy",
                        "ap",
                        "f1_weighted",
                        "jaccard_weighted",
                        "precision_weighted",
                        "recall_weighted",
                        "auc",
                    ]
            else:
                # No msle since it fails for negative values
                metric = ["mae", "mape", "mse", "r2", "rmse"]

        scores = pd.Series(name=self.name, dtype=float)
        for met in lst(metric):
            scorer = get_custom_scorer(met, pos_label=self._config.pos_label)
            scores[scorer.name] = self._get_score(scorer, rows=rows)

        return scores

    @crash
    def export_pipeline(self) -> Pipeline:
        """Export the transformer pipeline with final estimator.

        The returned pipeline is already fitted on the training set.
        Note that if the model used [automated feature scaling][],
        the [Scaler][] is added to the pipeline.

        Returns
        -------
        [Pipeline][]
            Current branch as a sklearn-like Pipeline object.

        """
        pipeline = deepcopy(self.pipeline)
        pipeline.steps.append((self._est_class.__name__, deepcopy(self.estimator)))
        return pipeline

    @composed(crash, method_to_log, beartype)
    def full_train(self, *, include_holdout: Bool = False):
        """Train the estimator on the complete dataset.

        In some cases, it might be desirable to use all available data
        to train a final model. Note that doing this means that the
        estimator can no longer be evaluated on the test set. The newly
        retrained estimator will replace the `estimator` attribute. If
        there is an active mlflow experiment, a new run is started
        with the name `[model_name]_full_train`. Since the estimator
        changed, the model is cleared.

        !!! warning
            Although the model is trained on the complete dataset, the
            pipeline is not. To get a fully trained pipeline, use:
            `pipeline = atom.export_pipeline().fit(atom.X, atom.y)`.

        Parameters
        ----------
        include_holdout: bool, default=False
            Whether to include the holdout set (if available) in the
            training of the estimator. It's discouraged to use this
            option since it means the model can no longer be evaluated
            on any set.

        """
        if include_holdout and self.holdout is None:
            raise ValueError("No holdout data set available.")

        if not include_holdout:
            X, y = self.X, self.y
        else:
            X = pd.concat([self.X, self.X_holdout])
            y = pd.concat([self.y, self.y_holdout])

        # Assign a mlflow run to the new estimator
        if self.experiment:
            self._run = mlflow.start_run(run_name=f"{self.name}_full_train")
            mlflow.end_run()

        self.fit(X, y)

    @available_if(lambda self: self.task is Task.binary_classification)
    @composed(crash, beartype)
    def get_best_threshold(
        self,
        metric: int | str | None = None,
        *,
        train_on_test: bool = False,
    ) -> Float:
        """Get the threshold that maximizes a metric.

        Uses sklearn's [TunedThresholdClassifierCV][] to post-tune the
        decision threshold (cut-off point) that is used for converting
        posterior probability estimates (i.e., output of `predict_proba`)
        or decision scores (i.e., output of `decision_function`) into a
        class label. The tuning is done by optimizing one of atom's
        metrics. The tuning estimator is stored under the `tuned_threshold`
        attribute. Only available for binary classifiers.

        !!! note
            By default, the threshold is optimized using the training
            set (which is already used for the initial training). This
            approach is subject to undesired overfitting. It's preferred
            to use `train_on_test=True`, which uses the test set for
            tuning, but only if there is another, independent set for
            testing ([holdout set][data-sets]).

        !!! tip
            Use the [plot_threshold][] method to visualize the effect
            of different thresholds on a metric.

        Parameters
        ----------
        metric: int, str or None, default=None
            Metric to optimize on. If None, the main metric is used.

        train_on_test: bool, default=False
            Whether to train the calibrator on the test set.

        Returns
        -------
        float
            Optimized threshold value.

        """
        if metric is None:
            scorer = self._metric[0]
        else:
            scorer = self._metric[self._get_metric(metric)[0]]

        self.tuned_threshold = TunedThresholdClassifierCV(
            estimator=self.estimator,
            scoring=scorer,
            n_jobs=self.n_jobs,
            random_state=self.random_state,
        )

        if not train_on_test:
            self.tuned_threshold.fit(self.X_train, self.y_train)
        else:
            self.tuned_threshold.fit(self.X_test, self.y_test)

        return self.tuned_threshold.best_threshold_

    @composed(crash, method_to_log, beartype)
    def inverse_transform(
        self,
        X: XSelector | None = None,
        y: YSelector | None = None,
        *,
        verbose: Verbose | None = None,
    ) -> YReturn | tuple[XReturn, YReturn]:
        """Inversely transform new data through the pipeline.

        Transformers that are only applied on the training set are
        skipped. The rest should all implement an `inverse_transform`
        method. If only `X` or only `y` is provided, it ignores
        transformers that require the other parameter. This can be
        of use to, for example, inversely transform only the target
        column. If called from a model that used automated feature
        scaling, the scaling is inverted as well.

        Parameters
        ----------
        X: dataframe-like or None, default=None
            Transformed feature set with shape=(n_samples, n_features).
            If None, `X` is ignored in the transformers.

        y: int, str, sequence, dataframe-like or None, default=None
            Target column(s) corresponding to `X`.

            - If None: `y` is ignored.
            - If int: Position of the target column in `X`.
            - If str: Name of the target column in `X`.
            - If sequence: Target column with shape=(n_samples,) or
              sequence of column names or positions for multioutput tasks.
            - If dataframe-like: Target columns for multioutput tasks.

        verbose: int or None, default=None
            Verbosity level for the transformers in the pipeline. If
            None, it uses the pipeline's verbosity.

        Returns
        -------
        dataframe
            Original feature set. Only returned if provided.

        series or dataframe
            Original target column. Only returned if provided.

        """
        Xt, yt = self._check_input(X, y, columns=self.branch.features, name=self.branch.target)

        with adjust(self.pipeline, transform=self.engine.data, verbose=verbose) as pl:
            return pl.inverse_transform(Xt, yt)

    @composed(crash, method_to_log, beartype)
    def register(
        self,
        name: str | None = None,
        stage: Stages = "None",
        *,
        archive_existing_versions: Bool = False,
    ):
        """Register the model in [mlflow's model registry][registry].

        This method is only available when model [tracking][] is
        enabled using one of the following URI schemes: databricks,
        http, https, postgresql, mysql, sqlite, mssql.

        Parameters
        ----------
        name: str or None, default=None
            Name for the registered model. If None, the model's full name
            is used. If the name of the model already exists, a new model
            version is created.

        stage: str, default="None"
            New desired stage for the model.

        archive_existing_versions: bool, default=False
            Whether all existing model versions in the `stage` will be
            moved to the "Archived" stage. Only valid when `stage` is
            "Staging" or "Production", otherwise an error will be raised.

        """
        if not self.experiment:
            raise PermissionError(
                "The register method is only available when "
                "there is a mlflow experiment active."
            )

        model = mlflow.register_model(
            model_uri=f"runs:/{self.run.info.run_id}/{self._est_class.__name__}",
            name=name or self.fullname,
            tags=self._ht["tags"] or None,
        )

        MlflowClient().transition_model_version_stage(
            name=model.name,
            version=model.version,
            stage=stage,
            archive_existing_versions=archive_existing_versions,
        )

    @composed(crash, method_to_log, beartype)
    def save_estimator(self, filename: str | Path = "auto"):
        """Save the estimator to a pickle file.

        Parameters
        ----------
        filename: str or Path, default="auto"
            Filename or [pathlib.Path][] of the file to save. Use
            "auto" for automatic naming.

        """
        if (path := Path(filename)).suffix != ".pkl":
            path = path.with_suffix(".pkl")

        if path.name == "auto.pkl":
            path = path.with_name(f"{self.estimator.__class__.__name__}.pkl")

        with open(path, "wb") as f:
            pickle.dump(self.estimator, f)

        self._log(f"{self.fullname} estimator successfully saved.", 1)

    @composed(crash, method_to_log, beartype)
    def serve(self, method: str = "predict"):
        """Serve the model as rest API endpoint for inference.

        The complete pipeline is served with the model. The inference
        data must be supplied as json to the HTTP request, e.g.
        `requests.get("http://127.0.0.1:8000/", json=X.to_json())`.
        The deployment is done on a [ray][] cluster. The default `host`
        and `port` parameters deploy to localhost.

        !!! tip
            Use `import ray; ray.serve.shutdown()` to close the
            endpoint after finishing.

        Parameters
        ----------
        method: str, default="predict"
            Estimator's method to do inference on.

        """
        check_dependency("ray")
        import ray
        from ray.serve import deployment, run

        @deployment
        class ServeModel:
            """Model deployment class.

            Parameters
            ----------
            pipeline: Pipeline
                Transformers + estimator to make inference on.

            method: str, default="predict"
                Estimator's method to do inference on.

            """

            def __init__(self, pipeline: Pipeline, method: str = "predict"):
                self.pipeline = pipeline
                self.method = method

            async def __call__(self, request: Request) -> np.ndarray:
                """Inference call.

                Parameters
                ----------
                request: Request.
                    HTTP request. It Should contain the rows to
                    predict in a json body.

                Returns
                -------
                np.ndarray
                    Model predictions.

                """
                payload = await request.json()
                return getattr(self.pipeline, self.method)(pd.read_json(payload))

        if not ray.is_initialized():
            ray.init(log_to_driver=False)

        run(ServeModel.bind(pipeline=self.export_pipeline(), method=method))

        self._log(f"Serving model {self.fullname}...", 1)

    @available_if(lambda self: self.task is Task.binary_classification)
    @composed(crash, method_to_log)
    def set_threshold(self, threshold: Float):
        """Set the binary threshold of the estimator.

        A new classifier using the new threshold replaces the `estimator`
        attribute. If there is an active mlflow experiment, a new run is
        started using the name `[model_name]_threshold_X`. Since the
        estimator changed, the model is [cleared][self-clear]. Only for
        binary classifiers.

        !!! tip
            Use the [get_best_threshold][self-get_best_threshold] method
            to find the optimal threshold for a specific metric.

        Parameters
        ----------
        threshold: float
            Binary threshold to classify the positive class.

        """
        if not 0 < threshold < 1:
            raise ValueError(
                "Invalid value for the threshold parameter. The value "
                f"should lie between 0 and 1, got {threshold}."
            )

        self._estimator = FixedThresholdClassifier(
            estimator=(est := deepcopy(self.estimator)),
            threshold=threshold,
            pos_label=self._config.pos_label,
        )

        # Add fitted estimator manually to avoid refitting
        self._estimator.estimator_ = est  # type: ignore[union-attr]

        # Assign a mlflow run to the new estimator
        if self.experiment:
            self._run = mlflow.start_run(run_name=f"{self.name}_threshold_{threshold}")
            mlflow.end_run()

        self.fit(self.X_train, self.y_train, prefit=True)

    @composed(crash, method_to_log, beartype)
    def transform(
        self,
        X: XSelector | None = None,
        y: YSelector | None = None,
        *,
        verbose: Verbose | None = None,
    ) -> YReturn | tuple[XReturn, YReturn]:
        """Transform new data through the pipeline.

        Transformers that are only applied on the training set are
        skipped. If only `X` or only `y` is provided, it ignores
        transformers that require the other parameter. This can be
        of use to, for example, transform only the target column. If
        called from a model that used automated feature scaling, the
        data is scaled as well.

        Parameters
        ----------
        X: dataframe-like or None, default=None
            Feature set with shape=(n_samples, n_features). If None,
            `X` is ignored. If None, `X` is ignored in the transformers.

        y: int, str, sequence, dataframe-like or None, default=None
            Target column(s) corresponding to `X`.

            - If None: `y` is ignored.
            - If int: Position of the target column in `X`.
            - If str: Name of the target column in `X`.
            - If sequence: Target column with shape=(n_samples,) or
              sequence of column names or positions for multioutput tasks.
            - If dataframe-like: Target columns for multioutput tasks.

        verbose: int or None, default=None
            Verbosity level for the transformers in the pipeline. If
            None, it uses the pipeline's verbosity.

        Returns
        -------
        dataframe
            Transformed feature set. Only returned if provided.

        series or dataframe
            Transformed target column. Only returned if provided.

        """
        Xt, yt = self._check_input(X, y, columns=self.og.features, name=self.og.target)

        with adjust(self.pipeline, transform=self.engine.data, verbose=verbose) as pl:
            return pl.transform(Xt, yt)


class ClassRegModel(BaseModel):
    """Classification and regression models."""

    @crash
    def get_tags(self) -> dict[str, Any]:
        """Get the model's tags.

        Return class parameters that provide general information about
        the model's characteristics.

        Returns
        -------
        dict
            Model's tags.

        """
        return {
            "acronym": self.acronym,
            "fullname": self.fullname,
            "estimator": self._est_class.__name__,
            "module": self._est_class.__module__,
            "handles_missing": getattr(self, "handles_missing", None),
            "needs_scaling": self.needs_scaling,
            "accepts_sparse": getattr(self, "accepts_sparse", None),
            "native_multilabel": self.native_multilabel,
            "native_multioutput": self.native_multioutput,
            "validation": self.validation,
            "supports_engines": ", ".join(getattr(self, "supports_engines", [])),
        }

    @overload
    def _prediction(
        self,
        X: RowSelector | XSelector,
        y: YSelector | None = ...,
        metric: str | MetricFunction | Scorer | None = ...,
        sample_weight: Sequence[Scalar] | None = ...,
        verbose: Verbose | None = ...,
        method: Literal[
            "decision_function",
            "predict",
            "predict_log_proba",
            "predict_proba",
        ] = ...,
    ) -> Pandas: ...

    @overload
    def _prediction(
        self,
        X: RowSelector | XSelector,
        y: YSelector | None,
        metric: str | MetricFunction | Scorer | None,
        sample_weight: Sequence[Scalar] | None,
        verbose: Verbose | None,
        method: Literal["score"],
    ) -> Float: ...

    def _prediction(
        self,
        X: RowSelector | XSelector,
        y: YSelector | None = None,
        metric: str | MetricFunction | Scorer | None = None,
        sample_weight: Sequence[Scalar] | None = None,
        verbose: Verbose | None = None,
        method: PredictionMethods = "predict",
    ) -> Float | Pandas:
        """Get predictions on new data or existing rows.

        New data is first transformed through the model's pipeline.
        Transformers that are only applied on the training set are
        skipped. The model should implement the provided method.

        Parameters
        ----------
        X: hashable, segment, sequence or dataframe-like
            [Selection of rows][row-and-column-selection] or feature
            set with shape=(n_samples, n_features) to make predictions
            on.

        y: int, str, sequence, dataframe-like or None, default=None
            Target column(s) corresponding to `X`.

            - If None: `y` is ignored.
            - If int: Position of the target column in `X`.
            - If str: Name of the target column in `X`.
            - If sequence: Target column with shape=(n_samples,) or
              sequence of column names or positions for multioutput
              tasks.
            - If dataframe: Target columns for multioutput tasks.

        metric: str, func, scorer or None, default=None
            Metric to calculate. Choose from any of sklearn's scorers,
            a function with signature metric(y_true, y_pred) or a scorer
            object. If None, it returns mean accuracy for classification
            tasks and r2 for regression tasks. Only for method="score".

        sample_weight: sequence or None, default=None
            Sample weights for the `score` method.

        verbose: int or None, default=None
            Verbosity level for the transformers in the pipeline. If
            None, it uses the pipeline's verbosity.

        method: str, default="predict"
            Prediction method to be applied to the estimator.

        Returns
        -------
        float, series or dataframe
            Calculated predictions. The return type depends on the method
            called.

        """

        def get_transform_X_y(
            X: XSelector,
            y: YSelector | None,
        ) -> tuple[pd.DataFrame, Pandas | None]:
            """Get X and y from the pipeline transformation.

            Parameters
            ----------
            X: dataframe-like
                Feature set.

            y: int, str, sequence, dataframe-like or None
                Target column(s) corresponding to `X`.

            Returns
            -------
            dataframe
                Transformed feature set.

            series, dataframe or None
                Transformed target column.

            """
            Xt, yt = self._check_input(X, y, columns=self.og.features, name=self.og.target)

            with adjust(self.pipeline, verbose=verbose) as pl:
                out = pl.transform(Xt, yt)

            return out if isinstance(out, tuple) else (out, yt)

        def assign_prediction_columns() -> list[str]:
            """Assign column names for the prediction methods.

            Returns
            -------
            list of str
                Columns for the dataframe.

            """
            if self.task.is_multioutput:
                return self.target  # When multioutput, target is list of str
            else:
                return self.mapping.get(self.target, np.unique(self.y).astype(str))

        try:
            if isinstance(X, pd.DataFrame):
                # Dataframe must go first since we can expect
                # prediction calls from dataframes with reset indices
                Xt, yt = get_transform_X_y(X, y)
            else:
                Xt, yt = self.branch._get_rows(X, return_X_y=True)  # type: ignore[call-overload]

                if self.scaler:
                    Xt = cast(pd.DataFrame, self.scaler.transform(Xt))

        except Exception:  # noqa: BLE001
            Xt, yt = get_transform_X_y(X, y)  # type: ignore[arg-type]

        if method != "score":
            pred = np.array(self.memory.cache(getattr(self.estimator, method))(Xt[self.features]))

            if pred.ndim == 1 or pred.shape[1] == 1:
                return to_series(pred, index=Xt.index, name=self.target)
            elif pred.ndim < 3:
                return to_df(pred, index=Xt.index, columns=assign_prediction_columns())
            elif self.task is Task.multilabel_classification:
                # Convert to (n_samples, n_targets)
                return pd.DataFrame(
                    data=np.array([d[:, 1] for d in pred]).T,
                    index=Xt.index,
                    columns=assign_prediction_columns(),
                )
            else:
                # Convert to (n_samples * n_classes, n_targets)
                return pd.DataFrame(
                    data=pred.reshape(-1, pred.shape[2]),
                    index=pd.MultiIndex.from_tuples(
                        [(col, idx) for col in np.unique(self.y) for idx in Xt.index]
                    ),
                    columns=assign_prediction_columns(),
                )

        else:
            if metric is None:
                scorer = self._metric[0]
            else:
                scorer = get_custom_scorer(metric, pos_label=self._config.pos_label)

            return self._score_from_est(
                scorer=scorer,
                estimator=self.estimator,
                X=Xt,
                y=yt,  # type: ignore[arg-type]
                sample_weight=sample_weight,
            )

    @available_if(estimator_has_attr("decision_function"))
    @composed(crash, method_to_log, beartype)
    def decision_function(
        self,
        X: RowSelector | XSelector,
        *,
        verbose: Verbose | None = None,
    ) -> YReturn:
        """Get confidence scores on new data or existing rows.

        New data is first transformed through the model's pipeline.
        Transformers that are only applied on the training set are
        skipped. The estimator must have a `decision_function` method.

        Read more in the [user guide][predicting].

        Parameters
        ----------
        X: hashable, segment, sequence or dataframe-like
            [Selection of rows][row-and-column-selection] or feature
            set with shape=(n_samples, n_features) to make predictions
            on.

        verbose: int or None, default=None
            Verbosity level for the transformers in the pipeline. If
            None, it uses the pipeline's verbosity.

        Returns
        -------
        series or dataframe
            Predicted confidence scores with shape=(n_samples,) for
            binary classification tasks (log likelihood ratio of the
            positive class) or shape=(n_samples, n_classes) for
            multiclass classification tasks.

        """
        return self._convert(self._prediction(X, verbose=verbose, method="decision_function"))

    @available_if(estimator_has_attr("predict"))
    @composed(crash, method_to_log, beartype)
    def predict(
        self,
        X: RowSelector | XSelector,
        *,
        inverse: Bool = True,
        verbose: Verbose | None = None,
    ) -> YReturn:
        """Get predictions on new data or existing rows.

        New data is first transformed through the model's pipeline.
        Transformers that are only applied on the training set are
        skipped. The estimator must have a `predict` method.

        Read more in the [user guide][predicting].

        Parameters
        ----------
        X: hashable, segment, sequence or dataframe-like
            [Selection of rows][row-and-column-selection] or feature
            set with shape=(n_samples, n_features) to make predictions
            on.

        inverse: bool, default=True
            Whether to inversely transform the output through the
            pipeline. This doesn't affect the predictions if there are
            no transformers in the pipeline or if the transformers have
            no `inverse_transform` method or don't apply to `y`.

        verbose: int or None, default=None
            Verbosity level for the transformers in the pipeline. If
            None, it uses the pipeline's verbosity.

        Returns
        -------
        series or dataframe
            Predictions with shape=(n_samples,) or shape=(n_samples,
            n_targets) for [multioutput tasks][].

        """
        pred = self._prediction(X, verbose=verbose, method="predict")

        if inverse:
            return self.inverse_transform(y=pred)
        else:
            return self._convert(pred)

    @available_if(estimator_has_attr("predict_log_proba"))
    @composed(crash, method_to_log, beartype)
    def predict_log_proba(
        self,
        X: RowSelector | XSelector,
        *,
        verbose: Verbose | None = None,
    ) -> XReturn:
        """Get class log-probabilities on new data or existing rows.

        New data is first transformed through the model's pipeline.
        Transformers that are only applied on the training set are
        skipped. The estimator must have a `predict_log_proba` method.

        Read more in the [user guide][predicting].

        Parameters
        ----------
        X: hashable, segment, sequence or dataframe-like
            [Selection of rows][row-and-column-selection] or feature
            set with shape=(n_samples, n_features) to make predictions
            on.

        verbose: int or None, default=None
            Verbosity level for the transformers in the pipeline. If
            None, it uses the pipeline's verbosity.

        Returns
        -------
        dataframe
            Predicted class log-probabilities with shape=(n_samples,
            n_classes) or shape=(n_samples * n_classes, n_targets) with
            a multiindex format for [multioutput tasks][].

        """
        return self._convert(self._prediction(X, verbose=verbose, method="predict_log_proba"))

    @available_if(estimator_has_attr("predict_proba"))
    @composed(crash, method_to_log, beartype)
    def predict_proba(
        self,
        X: RowSelector | XSelector,
        *,
        verbose: Verbose | None = None,
    ) -> XReturn:
        """Get class probabilities on new data or existing rows.

        New data is first transformed through the model's pipeline.
        Transformers that are only applied on the training set are
        skipped. The estimator must have a `predict_proba` method.

        Read more in the [user guide][predicting].

        Parameters
        ----------
        X: hashable, segment, sequence or dataframe-like
            [Selection of rows][row-and-column-selection] or feature
            set with shape=(n_samples, n_features) to make predictions
            on.

        verbose: int or None, default=None
            Verbosity level for the transformers in the pipeline. If
            None, it uses the pipeline's verbosity.

        Returns
        -------
        dataframe
            Predicted class probabilities with shape=(n_samples,
            n_classes) or shape=(n_samples * n_classes, n_targets) with
            a multiindex format for [multioutput tasks][].

        """
        return self._convert(self._prediction(X, verbose=verbose, method="predict_proba"))

    @available_if(estimator_has_attr("score"))
    @composed(crash, method_to_log, beartype)
    def score(
        self,
        X: RowSelector | XSelector,
        y: YSelector | None = None,
        *,
        metric: str | MetricFunction | Scorer | None = None,
        sample_weight: Sequence[Scalar] | None = None,
        verbose: Verbose | None = None,
    ) -> Float:
        """Get a metric score on new data.

        New data is first transformed through the model's pipeline.
        Transformers that are only applied on the training set are
        skipped.

        Read more in the [user guide][predicting].

        !!! info
            If the `metric` parameter is left to its default value, the
            method returns atom's metric score, not the metric returned
            by sklearn's score method for estimators.

        Parameters
        ----------
        X: hashable, segment, sequence or dataframe-like
            [Selection of rows][row-and-column-selection] or feature
            set with shape=(n_samples, n_features) to make predictions
            on.

        y: int, str, sequence, dataframe-like or None, default=None
            Target column(s) corresponding to `X`.

            - If None: `X` must be a selection of rows in the dataset.
            - If int: Position of the target column in `X`.
            - If str: Name of the target column in `X`.
            - If sequence: Target column with shape=(n_samples,) or
              sequence of column names or positions for multioutput
              tasks.
            - If dataframe: Target columns for multioutput tasks.

        metric: str, func, scorer or None, default=None
            Metric to calculate. Choose from any of sklearn's scorers,
            a function with signature `metric(y_true, y_pred) -> score`
            or a scorer object. If None, it uses atom's metric (the main
            metric for [multi-metric runs][]).

        sample_weight: sequence or None, default=None
            Sample weights corresponding to `y`.

        verbose: int or None, default=None
            Verbosity level for the transformers in the pipeline. If
            None, it uses the pipeline's verbosity.

        Returns
        -------
        float
            Metric score of X with respect to y.

        """
        return self._prediction(
            X=X,
            y=y,
            metric=metric,
            sample_weight=sample_weight,
            verbose=verbose,
            method="score",
        )


class ForecastModel(BaseModel):
    """Forecasting models."""

    @crash
    def get_tags(self) -> dict[str, Any]:
        """Get the model's tags.

        Return class parameters that provide general information about
        the model's characteristics.

        Returns
        -------
        dict
            Model's tags.

        """
        return {
            "acronym": self.acronym,
            "fullname": self.fullname,
            "estimator": self._est_class.__name__,
            "module": self._est_class.__module__,
            "handles_missing": getattr(self, "handles_missing", None),
            "multiple_seasonality": getattr(self, "multiple_seasonality", None),
            "native_multioutput": self.native_multioutput,
            "supports_engines": ", ".join(getattr(self, "supports_engines", ())),
        }

    @overload
    def _prediction(
        self,
        fh: RowSelector | ForecastingHorizon | None = ...,
        y: RowSelector | YSelector | None = ...,
        X: XSelector | None = ...,
        metric: str | MetricFunction | Scorer | None = ...,
        verbose: Verbose | None = ...,
        method: Literal[
            "predict",
            "predict_interval",
            "predict_proba",
            "predict_quantiles",
            "predict_residuals",
            "predict_var",
        ] = ...,
        **kwargs,
    ) -> Normal | Pandas: ...

    @overload
    def _prediction(
        self,
        fh: RowSelector | ForecastingHorizon | None,
        y: RowSelector | YSelector | None,
        X: XSelector | None,
        metric: str | MetricFunction | Scorer | None,
        verbose: Verbose | None,
        method: Literal["score"],
        **kwargs,
    ) -> Float: ...

    def _prediction(
        self,
        fh: RowSelector | ForecastingHorizon | None = None,
        y: RowSelector | YSelector | None = None,
        X: XSelector | None = None,
        metric: str | MetricFunction | Scorer | None = None,
        verbose: Verbose | None = None,
        method: PredictionMethodsTS = "predict",
        **kwargs,
    ) -> Float | Normal | Pandas:
        """Get predictions on new data or existing rows.

        If `fh` is not a [ForecastingHorizon][], it gets the rows from
        the branch. If `fh` is a [ForecastingHorizon][] or not provided,
        it converts `X` and `y` through the pipeline. The model should
        implement the provided method.

        Parameters
        ----------
        fh: hashable, segment, sequence, dataframe, [ForecastingHorizon][] or None, default=None
            The [forecasting horizon][row-and-column-selection] encoding
            the time stamps to forecast at.

        y: int, str, sequence, dataframe-like or None, default=None
            Ground truth observations.

        X: hashable, segment, sequence, dataframe-like or None, default=None
            Exogenous time series corresponding to `fh`.

        metric: str, func, scorer or None, default=None
            Metric to calculate. Choose from any of sklearn's scorers,
            a function with signature metric(y_true, y_pred) or a scorer
            object. If None, it returns mean accuracy for classification
            tasks and r2 for regression tasks. Only for method="score".

        verbose: int or None, default=None
            Verbosity level for the transformers in the pipeline. If
            None, it uses the pipeline's verbosity.

        method: str, default="predict"
            Prediction method to be applied to the estimator.

        **kwargs
            Additional keyword arguments for the method.

        Returns
        -------
        float, sktime.proba.[Normal][], series or dataframe
            Calculated predictions. The return type depends on the method
            called.

        """
        Xt: pd.DataFrame | None
        yt: Pandas | None

        if not isinstance(fh, ForecastingHorizon | None):
            try:
                Xt, yt = self.branch._get_rows(fh, return_X_y=True)

                if self.scaler:
                    Xt = cast(pd.DataFrame, self.scaler.transform(Xt))

                fh = ForecastingHorizon(Xt.index, is_relative=False)
            except IndexError:
                raise ValueError(
                    f"Ambiguous use of parameter fh, got {fh}. Use a ForecastingHorizon "
                    "object to make predictions on future samples outside the dataset."
                ) from None

        elif y is not None:
            try:
                Xt, yt = self.branch._get_rows(y, return_X_y=True)  # type: ignore[call-overload]

                if self.scaler and Xt is not None:
                    Xt = cast(pd.DataFrame, self.scaler.transform(Xt))

            except Exception:  # noqa: BLE001
                Xt, yt = self._check_input(X, y, columns=self.og.features, name=self.og.target)  # type: ignore[arg-type]

                with adjust(self.pipeline, verbose=verbose) as pl:
                    out = pl.transform(Xt, yt)

                Xt, yt = out if isinstance(out, tuple) else (Xt, out)

        elif X is not None:
            Xt, _ = self._check_input(X, columns=self.og.features, name=self.og.target)  # type: ignore[call-overload, arg-type]

            with adjust(self.pipeline, verbose=verbose) as pl:
                Xt = pl.transform(Xt)

        else:
            Xt, yt = X, y

        if method != "score":
            if "y" in sign(func := getattr(self.estimator, method)):
                return self.memory.cache(func)(y=yt, X=check_empty(Xt), **kwargs)
            else:
                return self.memory.cache(func)(fh=fh, X=check_empty(Xt), **kwargs)
        else:
            if metric is None:
                scorer = self._metric[0]
            else:
                scorer = get_custom_scorer(metric, pos_label=self._config.pos_label)

            return self._score_from_est(scorer, self.estimator, Xt, yt, **kwargs)  # type: ignore[arg-type]

    @composed(crash, method_to_log, beartype)
    def predict(
        self,
        fh: RowSelector | ForecastingHorizon,
        X: XSelector | None = None,
        *,
        inverse: Bool = True,
        verbose: Verbose | None = None,
    ) -> YReturn:
        """Get predictions on new data or existing rows.

        New data is first transformed through the model's pipeline.
        Transformers that are only applied on the training set are
        skipped. The estimator must have a `predict` method.

        Read more in the [user guide][predicting].

        Parameters
        ----------
        fh: hashable, segment, sequence, dataframe or [ForecastingHorizon][]
            The [forecasting horizon][row-and-column-selection] encoding
            the time stamps to forecast at.

        X: hashable, segment, sequence, dataframe-like or None, default=None
            Exogenous time series corresponding to `fh`.

        inverse: bool, default=True
            Whether to inversely transform the output through the
            pipeline. This doesn't affect the predictions if there are
            no transformers in the pipeline or if the transformers have
            no `inverse_transform` method or don't apply to `y`.

        verbose: int or None, default=None
            Verbosity level for the transformers in the pipeline. If
            None, it uses the pipeline's verbosity.

        Returns
        -------
        series or dataframe
            Predictions with shape=(n_samples,) or shape=(n_samples,
            n_targets) for [multivariate][] tasks.

        """
        pred = self._prediction(fh=fh, X=X, verbose=verbose, method="predict")

        if inverse:
            return self.inverse_transform(y=pred)
        else:
            return self._convert(pred)

    @composed(crash, method_to_log, beartype)
    def predict_interval(
        self,
        fh: RowSelector | ForecastingHorizon,
        X: XSelector | None = None,
        *,
        coverage: Float | Sequence[Float] = 0.9,
        inverse: Bool = True,
        verbose: Verbose | None = None,
    ) -> XReturn:
        """Get prediction intervals on new data or existing rows.

        New data is first transformed through the model's pipeline.
        Transformers that are only applied on the training set are
        skipped. The estimator must have a `predict_interval` method.

        Read more in the [user guide][predicting].

        Parameters
        ----------
        fh: hashable, segment, sequence, dataframe or [ForecastingHorizon][]
            The [forecasting horizon][row-and-column-selection] encoding
            the time stamps to forecast at.

        X: hashable, segment, sequence, dataframe-like or None, default=None
            Exogenous time series corresponding to `fh`.

        coverage: float or sequence, default=0.9
            Nominal coverage(s) of predictive interval(s).

        inverse: bool, default=True
            Whether to inversely transform the output through the
            pipeline. This doesn't affect the predictions if there are
            no transformers in the pipeline or if the transformers have
            no `inverse_transform` method or don't apply to `y`.

        verbose: int or None, default=None
            Verbosity level for the transformers in the pipeline. If
            None, it uses the pipeline's verbosity.

        Returns
        -------
        dataframe
            Computed interval forecasts.

        """
        pred = self._prediction(
            fh=fh,
            X=X,
            coverage=coverage,
            verbose=verbose,
            method="predict_interval",
        )

        if inverse:
            new_interval = pd.DataFrame(index=pred.index, columns=pred.columns)

            # We pass every level of the multiindex to inverse_transform...
            for cover in pred.columns.levels[1]:  # type: ignore[union-attr]
                for level in pred.columns.levels[2]:  # type: ignore[union-attr]
                    # Select only the lower or upper level columns
                    curr_cover = pred.columns.get_level_values(1)
                    curr_level = pred.columns.get_level_values(2)
                    df = pred.loc[:, (curr_cover == cover) & (curr_level == level)]

                    # Use original columns names
                    df.columns = df.columns.droplevel(level=(1, 2))

                    # Apply inverse transformation
                    for name, column in self.inverse_transform(y=df).items():
                        new_interval.loc[:, (name, cover, level)] = column

            return self._convert(new_interval)
        else:
            return self._convert(pred)

    @composed(crash, method_to_log, beartype)
    def predict_proba(
        self,
        fh: RowSelector | ForecastingHorizon,
        X: XSelector | None = None,
        *,
        marginal: Bool = True,
        verbose: Verbose | None = None,
    ) -> Normal:
        """Get probabilistic forecasts on new data or existing rows.

        New data is first transformed through the model's pipeline.
        Transformers that are only applied on the training set are
        skipped. The estimator must have a `predict_proba` method.

        Read more in the [user guide][predicting].

        Parameters
        ----------
        fh: hashable, segment, sequence, dataframe or [ForecastingHorizon][]
            The [forecasting horizon][row-and-column-selection] encoding
            the time stamps to forecast at.

        X: hashable, segment, sequence, dataframe-like or None, default=None
            Exogenous time series corresponding to `fh`.

        marginal: bool, default=True
            Whether returned distribution is marginal by time index.

        verbose: int or None, default=None
            Verbosity level for the transformers in the pipeline. If
            None, it uses the pipeline's verbosity.

        Returns
        -------
        sktime.proba.[Normal][]
            Distribution object.

        """
        return self._prediction(
            fh=fh,
            X=X,
            marginal=marginal,
            verbose=verbose,
            method="predict_proba",
        )

    @composed(crash, method_to_log, beartype)
    def predict_quantiles(
        self,
        fh: RowSelector | ForecastingHorizon,
        X: XSelector | None = None,
        *,
        alpha: Float | Sequence[Float] = (0.05, 0.95),
        verbose: Verbose | None = None,
    ) -> XReturn:
        """Get quantile forecasts on new data or existing rows.

        New data is first transformed through the model's pipeline.
        Transformers that are only applied on the training set are
        skipped. The estimator must have a `predict_quantiles` method.

        Read more in the [user guide][predicting].

        Parameters
        ----------
        fh: hashable, segment, sequence, dataframe or [ForecastingHorizon][]
            The [forecasting horizon][row-and-column-selection] encoding
            the time stamps to forecast at.

        X: hashable, segment, sequence, dataframe-like or None, default=None
            Exogenous time series corresponding to `fh`.

        alpha: float or sequence, default=(0.05, 0.95)
            A probability or list of, at which quantile forecasts are
            computed.

        verbose: int or None, default=None
            Verbosity level for the transformers in the pipeline. If
            None, it uses the pipeline's verbosity.

        Returns
        -------
        dataframe
            Computed quantile forecasts.

        """
        return self._convert(
            self._prediction(
                fh=fh,
                X=X,
                alpha=alpha,
                verbose=verbose,
                method="predict_quantiles",
            )
        )

    @composed(crash, method_to_log, beartype)
    def predict_residuals(
        self,
        y: RowSelector | YConstructor,
        X: XSelector | None = None,
        *,
        verbose: Verbose | None = None,
    ) -> YReturn:
        """Get residuals of forecasts on new data or existing rows.

        New data is first transformed through the model's pipeline.
        Transformers that are only applied on the training set are
        skipped. The estimator must have a `predict_residuals` method.

        Read more in the [user guide][predicting].

        Parameters
        ----------
        y: hashable, segment, sequence or dataframe-like
            [Selection of rows][row-and-column-selection] or ground
            truth observations.

        X: dataframe-like or None, default=None
            Exogenous time series corresponding to `y`. This parameter
            is ignored outif `y` is a selection of rows in the dataset.

        verbose: int or None, default=None
            Verbosity level for the transformers in the pipeline. If
            None, it uses the pipeline's verbosity.

        Returns
        -------
        series or dataframe
            Residuals with shape=(n_samples,) or shape=(n_samples,
            n_targets) for [multivariate][] tasks.

        """
        return self._convert(
            self._prediction(y=y, X=X, verbose=verbose, method="predict_residuals")
        )

    @composed(crash, method_to_log, beartype)
    def predict_var(
        self,
        fh: RowSelector | ForecastingHorizon,
        X: XSelector | None = None,
        *,
        cov: Bool = False,
        verbose: Verbose | None = None,
    ) -> XReturn:
        """Get variance forecasts on new data or existing rows.

        New data is first transformed through the model's pipeline.
        Transformers that are only applied on the training set are
        skipped. The estimator must have a `predict_var` method.

        Read more in the [user guide][predicting].

        Parameters
        ----------
        fh: hashable, segment, sequence, dataframe or [ForecastingHorizon][]
            The [forecasting horizon][row-and-column-selection] encoding
            the time stamps to forecast at.

        X: hashable, segment, sequence, dataframe-like or None, default=None
            Exogenous time series corresponding to `fh`.

        cov: bool, default=False
            Whether to compute covariance matrix forecast or marginal
            variance forecasts.

        verbose: int or None, default=None
            Verbosity level for the transformers in the pipeline. If
            None, it uses the pipeline's verbosity.

        Returns
        -------
        dataframe
            Computed variance forecasts.

        """
        return self._convert(
            self._prediction(
                fh=fh,
                X=X,
                cov=cov,
                verbose=verbose,
                method="predict_var",
            )
        )

    @composed(crash, method_to_log, beartype)
    def score(
        self,
        y: RowSelector | YSelector,
        X: XSelector | None = None,
        fh: RowSelector | ForecastingHorizon | None = None,
        *,
        metric: str | MetricFunction | Scorer | None = None,
        verbose: Verbose | None = None,
    ) -> Float:
        """Get a metric score on new data.

        New data is first transformed through the model's pipeline.
        Transformers that are only applied on the training set are
        skipped.

        Read more in the [user guide][predicting].

        !!! info
            If the `metric` parameter is left to its default value, the
            method returns atom's metric score, not the metric used by
            sktime's score method for estimators.

        Parameters
        ----------
        y: int, str, sequence or dataframe-like
            [Selection of rows][row-and-column-selection] or ground
            truth observations.

        X: dataframe-like or None, default=None
            Exogenous time series corresponding to `fh`. This parameter
            is ignored if `y` is a selection of rows in the dataset.

        fh: hashable, segment, sequence, dataframe, [ForecastingHorizon][] or None, default=None
            Do nothing. The forecast horizon is taken from the index of
            `y`. Implemented for continuity of sktime's API.

        metric: str, func, scorer or None, default=None
            Metric to calculate. Choose from any of sklearn's scorers,
            a function with signature `metric(y_true, y_pred) -> score`
            or a scorer object. If None, it uses atom's metric (the main
            metric for [multi-metric runs][]).

        verbose: int or None, default=None
            Verbosity level for the transformers in the pipeline. If
            None, it uses the pipeline's verbosity.

        Returns
        -------
        float
            Metric score of `y` with respect to a ground truth.

        """
        return self._prediction(fh=None, y=y, X=X, metric=metric, verbose=verbose, method="score")
