"""Automated Tool for Optimized Modeling (ATOM).

Author: Mavs
Description: Module containing the BaseTrainer class.

"""

from __future__ import annotations

import traceback
from abc import ABCMeta
from datetime import datetime as dt
from typing import Any

import mlflow
import numpy as np
from joblib import Parallel, delayed
from optuna import Study, create_study

from atom.baserunner import BaseRunner
from atom.data import BranchManager
from atom.data_cleaning import BaseTransformer
from atom.models import MODELS, create_custom_model
from atom.plots import RunnerPlot
from atom.utils.types import Model, Verbose, sequence_t
from atom.utils.utils import (
    ClassMap, DataConfig, Goal, Task, adjust, check_dependency,
    get_custom_scorer, lst, sign, time_to_str,
)


class BaseTrainer(BaseRunner, RunnerPlot, metaclass=ABCMeta):
    """Base class for trainers.

    Implements methods to check the validity of the parameters,
    create models and metrics, run hyperparameter tuning, model
    training, bootstrap, and display the final results.

    See training.py for a description of the parameters.

    """

    def __init__(
        self, models, metric, est_params, n_trials, ht_params, n_bootstrap,
        parallel, errors, n_jobs, device, engine, backend, memory, verbose,
        warnings, logger, experiment, random_state,
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

        self.est_params = est_params
        self.n_trials = n_trials
        self.ht_params = ht_params
        self.n_bootstrap = n_bootstrap
        self.parallel = parallel
        self.errors = errors

        self._models = lst(models) if models is not None else ClassMap()
        self._metric = lst(metric) if metric is not None else ClassMap()

        self._config = DataConfig(index=self._goal is Goal.forecast)
        self._branches = BranchManager(memory=self.memory)

        self._n_trials = {}
        self._n_bootstrap = {}
        self._ht_params = {"distributions": {}, "cv": 1, "plot": False, "tags": {}}

    def _check_param(self, param: str, value: Any) -> dict:
        """Check the validity of one parameter.

        Parameters accept three formats:

        - dict: Each key is the name of a model, and the value applies
          only to that model.
        - sequence: The N-th element applies to the N-th model. Has to
          have the same length as the models.
        - value: Same value applies to all models.

        Parameters
        ----------
        param: str
            Name of the parameter to check.

        value: Any
            Value of the parameter.

        Returns
        -------
        dict
            Parameter with model names as keys.

        """
        if isinstance(value, sequence_t):
            if len(value) != len(self._models):
                raise ValueError(
                    f"Invalid value for the {param} parameter. The length "
                    "should be equal to the number of models, got len"
                    f"(models)={len(self._models)} and len({param})={len(value)}."
                )
            return dict(zip(lst(self.models), value, strict=True))
        elif not isinstance(value, dict):
            return {k: value for k in lst(self.models)}

        return value

    def _prepare_parameters(self):
        """Check the validity of the input parameters.

        Creates the models, assigns a metric, prepares the estimator's
        parameters and the parameters for hyperparameter tuning.

        """
        # Define metric ============================================ >>

        # Assign default scorer
        if not self._metric:
            if self.task.is_classification:
                if self.task is Task.binary_classification:
                    # Binary classification
                    scorer = get_custom_scorer("f1", pos_label=self._config.pos_label)
                elif self.task.is_multiclass:
                    # Multiclass, multiclass-multioutput classification
                    scorer = get_custom_scorer("f1_weighted", pos_label=self._config.pos_label)
                elif self.task is Task.multilabel_classification:
                    # Multilabel classification
                    scorer = get_custom_scorer("ap", pos_label=self._config.pos_label)
            elif self.task.is_regression:
                # Regression, multioutput regression
                scorer = get_custom_scorer("r2", pos_label=self._config.pos_label)
            elif self.task.is_forecast:
                # Forecasting
                scorer = get_custom_scorer("mape", pos_label=self._config.pos_label)

            self._metric = ClassMap(scorer)

        elif not isinstance(self._metric, ClassMap):
            metrics = []
            for m in lst(self._metric):
                if isinstance(m, str):
                    metrics.extend(m.split("+"))
                else:
                    metrics.append(m)

            self._metric = ClassMap(
                get_custom_scorer(m, pos_label=self._config.pos_label) for m in metrics
            )

        # Define models ============================================ >>

        kwargs = {
            "goal": self._goal,
            "config": self._config,
            "branches": self._branches,
            "metric": self._metric,
            **{attr: getattr(self, attr) for attr in BaseTransformer.attrs},
        }

        inc = []
        exc = []
        for model in self._models:
            if isinstance(model, str):
                for m in model.split("+"):
                    if m.startswith("!"):
                        exc.append(m[1:].lower())
                        continue

                    try:
                        if len(name := m.split("_", 1)) > 1:
                            name, tag = name[0].lower(), f"_{name[1]}"
                        else:
                            name, tag = name[0].lower(), ""

                        cls = next(n for n in MODELS if n.acronym.lower() == name)

                    except StopIteration:
                        raise ValueError(
                            f"Invalid value for the models parameter, got {m}. "
                            "Note that tags must be separated by an underscore. "
                            "Available model are:\n" +
                            "\n".join(
                                [
                                    f" --> {m.__name__} ({m.acronym})"
                                    for m in MODELS
                                    if self._goal.name in m._estimators
                                ]
                            )
                        ) from None

                    # Check if libraries for non-sklearn models are available
                    dependencies = {
                        "BATS": "tbats",
                        "CatB": "catboost",
                        "LGB": "lightgbm",
                        "MSTL": "statsforecast",
                        "TBATS": "tbats",
                        "XGB": "xgboost",
                    }
                    if cls.acronym in dependencies:
                        check_dependency(dependencies[cls.acronym])

                    # Check if the model supports the task
                    if self._goal.name not in cls._estimators:
                        # Forecast task can use regression models
                        if self._goal is not Goal.forecast or "regression" not in cls._estimators:
                            raise ValueError(
                                f"The {cls.__name__} model is not "
                                f"available for {self.task.name} tasks!"
                            )

                    inc.append(cls(name=f"{cls.acronym}{tag}", **kwargs))

            elif isinstance(model, Model):  # For new instances or reruns
                inc.append(model)

            else:  # Model is a custom estimator
                inc.append(create_custom_model(estimator=model, **kwargs))

        if inc and exc:
            raise ValueError(
                "Invalid value for the models parameter. You can either "
                "include or exclude models, not combinations of these."
            )
        elif inc:
            if len(set(names := [m.name for m in inc])) != len(names):
                raise ValueError(
                    "Invalid value for the models parameter. There are duplicate "
                    "models. Add a tag to a model's acronym (separated by an "
                    "underscore) to train two different models with the same estimator, "
                    "e.g., models=['LR_1', 'LR_2']."
                )
            self._models = ClassMap(*inc)
        else:
            self._models = ClassMap(
                model(**kwargs) for model in MODELS
                if self._goal.name in model._estimators and model.acronym.lower() not in exc
            )

        # Prepare est_params ======================================= >>

        if self.est_params is not None:
            for model in self._models:
                params = {}
                for key, value in self.est_params.items():
                    # Parameters for this model only
                    if key.lower() == model.name.lower() or key.lower() == "all":
                        params.update(value)
                    # Parameters for all models
                    elif key not in self._models:
                        params.update({key: value})

                for key, value in params.items():
                    if key.endswith("_fit"):
                        model._est_params_fit[key[:-4]] = value
                    else:
                        model._est_params[key] = value

        # Prepare ht parameters ==================================== >>

        self._n_trials = self._check_param("n_trials", self.n_trials)
        self._n_bootstrap = self._check_param("n_bootstrap", self.n_bootstrap)
        self._ht_params.update(self.ht_params or {})
        for key, value in self._ht_params.items():
            if key in ("cv", "plot"):
                self._ht_params[key] = self._check_param(key, value)
            elif key == "tags":
                self._ht_params[key] = {name: {} for name in lst(self.models)}
                for name in self._models.keys():
                    for k, v in self._check_param(key, value).items():
                        if k.lower() == name.lower() or k.lower() == "all":
                            self._ht_params[key][name].update(v)
                        elif k not in self._models.keys():
                            self._ht_params[key][name][k] = v
            elif key == "distributions":
                self._ht_params[key] = {name: {} for name in self._models.keys()}
                for name in self._models.keys():
                    if not isinstance(value, dict):
                        # If sequence, it applies to all models
                        self._ht_params[key][name] = {k: None for k in lst(value)}
                    else:
                        # Either one distribution for all or per model
                        for k, v in value.items():
                            if k.lower() == name.lower() or k.lower() == "all":
                                if isinstance(v, dict):
                                    self._ht_params[key][name].update(v)
                                else:
                                    self._ht_params[key][name].update(
                                        {param: None for param in lst(v)}
                                    )
                            elif k not in self._models:
                                self._ht_params[key][name][k] = v
            elif key in sign(create_study) | sign(Study.optimize):
                self._ht_params[key] = {k: value for k in self._models.keys()}
            else:
                raise ValueError(
                    f"Invalid value for the ht_params parameter. Key {key} is invalid."
                )

    def _core_iteration(self):
        """Fit and evaluate all models and displays final results."""

        def execute_model(m: Model, verbose: Verbose | None = None) -> Model | None:
            """Execute a single model.

            Runs hyperparameter tuning, training and bootstrap for one
            model. Function needed for parallelization.

            Parameters
            ----------
            m: Model
                Model to train and evaluate.

            verbose: int or None, default=None
                Verbosity level for the estimator. If None, it leaves it to
                its original verbosity.

            Returns
            -------
            Model or None
                Trained model. Returns None when the model raised an
                exception and error=="skip".

            """
            try:
                # Set BaseTransformer params in new nodes
                self.experiment = self.experiment  # Set mlflow experiment
                self.logger = self.logger  # Reassign logger's handlers
                m.logger = m.logger

                self._log("\n", 1)  # Separate output from header

                with adjust(m, verbose=verbose):
                    # If it has predefined or custom dimensions, run the ht
                    m._ht = {k: v[m._group] for k, v in self._ht_params.items()}
                    if self._n_trials[m._group] > 0:
                        if m._ht["distributions"] or hasattr(m, "_get_distributions"):
                            m.hyperparameter_tuning(self._n_trials[m._group])

                    m.fit()

                    if self._n_bootstrap[m._group]:
                        m.bootstrapping(self._n_bootstrap[m._group])

                    self._log("-" * 49 + f"\nTime: {time_to_str(m.results['time'])}", 1)

                return m

            except Exception as ex:
                self._log(f"\nException encountered while running the {m.name} model.", 1)
                self._log("".join(traceback.format_tb(ex.__traceback__))[:-1], 3)
                self._log(f"{ex.__class__.__name__}: {ex}", 1)

                if self.experiment:
                    mlflow.end_run()
                    if self.errors != "keep":
                        mlflow.delete_run(m.run.info.run_id)

                if self.errors == "keep":
                    return m
                elif self.errors == "skip":
                    return None
                else:
                    raise ex

        t = dt.now()  # Measure the time the whole pipeline takes

        if self.parallel and len(self._models) > 1:
            if self.backend == "ray":
                import ray

                # This implementation is more efficient than through joblib's
                # ray backend. The difference is that in this one you start N
                # tasks, and in the other, you start N actors and then have them
                # each run the function
                execute_remote = ray.remote(num_cpus=self.n_jobs)(execute_model)
                models = ray.get([execute_remote.remote(m, 0) for m in self._models])
            elif self.backend == "dask":
                import dask

                models = dask.compute(*[dask.delayed(execute_model)(m, 0) for m in self._models])
            else:
                models = Parallel(n_jobs=self.n_jobs)(
                    delayed(execute_model)(m) for m in self._models
                )
        else:
            models = [model for m in self._models if (model := execute_model(m))]

        self._models = ClassMap(m for m in models if m)

        if not self._models:
            raise RuntimeError(
                "All models failed to run. Use the logger to investigate the "
                "exceptions or set parameter errors='raise' to raise the exception."
            )

        self._log(f"\n\nFinal results {'=' * 20} >>", 1)
        self._log(f"Total time: {time_to_str((dt.now() - t).total_seconds())}", 1)
        self._log("-" * 37, 1)

        maxlen = 0
        names, scores = [], []
        for m in self._models:
            # Add the model name for repeated model classes
            if len(list(filter(lambda x: x.acronym == m.acronym, self._models))) > 1:
                names.append(f"{m.fullname} ({m.name})")
            else:
                names.append(m.fullname)

            try:
                scores.append(m._best_score())
            except (ValueError, AttributeError):  # Fails when errors="keep"
                scores.append(-np.inf)

            maxlen = max(maxlen, len(names[-1]))

        for i, m in enumerate(self._models):
            out = f"{names[i]:{maxlen}s} --> {m._final_output()}"
            if scores[i] == max(scores) and len(self._models) > 1:
                out += " !"

            self._log(out, 1)
