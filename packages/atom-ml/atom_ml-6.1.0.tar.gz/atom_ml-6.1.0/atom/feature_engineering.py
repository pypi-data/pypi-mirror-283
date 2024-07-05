"""Automated Tool for Optimized Modeling (ATOM).

Author: Mavs
Description: Module containing the feature engineering transformers.

"""

from __future__ import annotations

from collections.abc import Hashable
from random import sample
from typing import Any, Literal, cast

import featuretools as ft
import numpy as np
import pandas as pd
from beartype import beartype
from gplearn.genetic import SymbolicTransformer
from scipy import stats
from sklearn.base import is_classifier
from sklearn.feature_selection import (
    RFE, RFECV, SelectFromModel, SelectKBest, SequentialFeatureSelector, chi2,
    f_classif, f_regression, mutual_info_classif, mutual_info_regression,
)
from sklearn.model_selection import cross_val_score
from sklearn.utils.validation import _check_feature_names_in
from typing_extensions import Self
from zoofs import (
    DragonFlyOptimization, GeneticOptimization, GreyWolfOptimization,
    HarrisHawkOptimization, ParticleSwarmOptimization,
)

from atom.basetransformer import BaseTransformer
from atom.data_cleaning import Scaler, TransformerMixin
from atom.utils.types import (
    Bool, Engine, FeatureSelectionSolvers, FeatureSelectionStrats,
    FloatLargerEqualZero, FloatLargerZero, FloatZeroToOneInc,
    IntLargerEqualZero, IntLargerZero, NJobs, Operators, Scalar, Sequence,
    Verbose, XConstructor, XReturn, YConstructor,
)
from atom.utils.utils import (
    Goal, Task, check_is_fitted, check_scaling, get_custom_scorer, is_sparse,
    lst, merge, sign, to_df, to_tabular,
)


@beartype
class FeatureExtractor(TransformerMixin):
    """Extract features from datetime columns.

    Create new features extracting datetime elements (day, month,
    year, etc...) from the provided columns. Columns of dtype
    `datetime64` are used as is. Categorical columns that can be
    successfully converted to a datetime format (less than 30% NaT
    values after conversion) are also used.

    This class can be accessed from atom through the [feature_extraction]
    [atomclassifier-feature_extraction] method. Read more in the
    [user guide][extracting-datetime-features].

    !!! warning
        Decision trees based algorithms build their split rules
        according to one feature at a time. This means that they will
        fail to correctly process cyclic features since the sin/cos
        features should be considered one single coordinate system.

    Parameters
    ----------
    features: str or sequence, default=("year", "month", "day")
        Features to create from the datetime columns. Note that
        created features with zero variance (e.g., the feature hour
        in a column that only contains dates) are ignored. Allowed
        values are datetime attributes from `pandas.Series.dt`.

    fmt: str, dict or None, default=None
        Format (`strptime`) of the categorical columns that need
        to be converted to datetime. If dict, use the column's name
        as key and the format as value. If None, the format is
        inferred automatically from the first non NaN value. Values
        that cannot be converted are returned as `NaT`.

    encoding_type: str, default="ordinal"
        Type of encoding to use. Choose from:

        - "ordinal": Encode features in increasing order.
        - "cyclic": Encode features using sine and cosine to capture
          their cyclic nature. This approach creates two columns for
          every feature. Non-cyclic features still use ordinal encoding.

    from_index: bool, default=False
        Whether to use the index as the datetime column to convert.

    drop_columns: bool, default=True
        Whether to drop the original columns after transformation. This
        parameter is ignored if `from_index=True`.

    verbose: int, default=0
        Verbosity level of the class. Choose from:

        - 0 to not print anything.
        - 1 to print basic information.
        - 2 to print detailed information.

    Attributes
    ----------
    feature_names_in_: np.ndarray
        Names of features seen during `fit`.

    n_features_in_: int
        Number of features seen during `fit`.

    See Also
    --------
    atom.feature_engineering:FeatureGenerator
    atom.feature_engineering:FeatureGrouper
    atom.feature_engineering:FeatureSelector

    Examples
    --------
    === "atom"
        ```pycon
        import pandas as pd
        from atom import ATOMClassifier
        from sklearn.datasets import load_breast_cancer

        X, y = load_breast_cancer(return_X_y=True, as_frame=True)

        # Add a datetime column
        X["date"] = pd.date_range(start="1/1/2018", periods=len(X))

        atom = ATOMClassifier(X, y)
        atom.feature_extraction(features=["day"], fmt="%d/%m/%Y", verbose=2)

        # Note the date_day column
        print(atom.dataset)
        ```

    === "stand-alone"
        ```pycon
        import pandas as pd
        from atom.feature_engineering import FeatureExtractor
        from sklearn.datasets import load_breast_cancer

        X, _ = load_breast_cancer(return_X_y=True, as_frame=True)

        # Add a datetime column
        X["date"] = pd.date_range(start="1/1/2018", periods=len(X))

        fe = FeatureExtractor(features=["day"], fmt="%Y-%m-%d", verbose=2)
        X = fe.transform(X)

        # Note the date_day column
        print(X)
        ```

    """

    def __init__(
        self,
        features: str | Sequence[str] = ("year", "month", "day"),
        fmt: str | dict[str, str] | None = None,
        *,
        encoding_type: Literal["ordinal", "cyclic"] = "ordinal",
        drop_columns: Bool = True,
        from_index: Bool = False,
        verbose: Verbose = 0,
    ):
        super().__init__(verbose=verbose)
        self.fmt = fmt
        self.features = features
        self.encoding_type = encoding_type
        self.drop_columns = drop_columns
        self.from_index = from_index

    def transform(self, X: XConstructor, y: YConstructor | None = None) -> XReturn:
        """Extract the new features.

        Parameters
        ----------
        X: dataframe-like
            Feature set with shape=(n_samples, n_features).

        y: sequence, dataframe-like or None, default=None
            Do nothing. Implemented for continuity of the API.

        Returns
        -------
        dataframe
            Transformed feature set.

        """
        Xt = to_df(X, columns=getattr(self, "feature_names_in_", None))

        self._log("Extracting datetime features...", 1)

        if self.from_index:
            if hasattr(Xt.index, "to_timestamp"):
                Xc = pd.DataFrame(Xt.index.to_timestamp())
                order = Xc.columns.tolist() + Xt.columns.tolist()
            else:
                raise ValueError("Unable to convert the index to a timestamp format.")
        else:
            Xc = Xt.select_dtypes(exclude="number")
            order = Xt.columns.tolist()

        X_new = pd.DataFrame(index=Xt.index)
        for name, column in Xc.items():
            col_dt = pd.to_datetime(
                arg=column,
                errors="coerce",  # Converts to NaT if he can't format
                format=self.fmt.get(str(name)) if isinstance(self.fmt, dict) else self.fmt,
            )

            # If >30% values are NaT, the conversion was unsuccessful
            if col_dt.isna().sum() / len(Xc) >= 0.3:
                continue  # Skip this column

            self._log(f" --> Extracting features from column {name}.", 1)

            # Extract features from the datetime column
            # Reverse to keep the provided order of features
            for fx in map(str.lower, reversed(lst(self.features))):
                if hasattr(col_dt.dt, fx.lower()):
                    series = getattr(col_dt.dt, fx)
                else:
                    raise ValueError(
                        "Invalid value for the feature parameter. Value "
                        f"{fx.lower()} is not an attribute of pd.Series.dt."
                    )

                if not isinstance(series, pd.Series):
                    self._log(
                        f"   --> Extracting feature {fx} "
                        "failed. Result is not a Series.dt.", 2,
                    )
                    continue  # Skip if the information is not present in the format
                elif (series == series[0]).all():
                    continue  # Skip if the resulting feature has zero variance

                min_val: int = 0
                max_val: Scalar | pd.Series | None = None  # None if isn't cyclic
                if self.encoding_type == "cyclic":
                    if fx == "microsecond":
                        min_val, max_val = 0, 1e6 - 1
                    elif fx in ("second", "minute"):
                        min_val, max_val = 0, 59
                    elif fx == "hour":
                        min_val, max_val = 0, 23
                    elif fx in ("weekday", "dayofweek", "day_of_week"):
                        min_val, max_val = 0, 6
                    elif fx in ("day", "dayofmonth", "day_of_month"):
                        min_val, max_val = 1, col_dt.dt.daysinmonth
                    elif fx in ("dayofyear", "day_of_year"):
                        min_val = 1
                        max_val = pd.Series([365 if i else 366 for i in col_dt.dt.is_leap_year])
                    elif fx == "month":
                        min_val, max_val = 1, 12
                    elif fx == "quarter":
                        min_val, max_val = 1, 4

                new_name = f"{name}_{fx}"
                if self.encoding_type == "ordinal" or max_val is None:
                    self._log(f"   --> Creating feature {new_name}.", 2)
                    X_new[new_name] = series.to_numpy()
                    order.insert(order.index(str(name)) + 1, new_name)
                elif self.encoding_type == "cyclic":
                    self._log(f"   --> Creating cyclic feature {new_name}.", 2)
                    pos = 2 * np.pi * (series.to_numpy() - min_val) / np.array(max_val)
                    X_new[f"{new_name}_sin"] = np.sin(pos)
                    X_new[f"{new_name}_cos"] = np.cos(pos)
                    order.insert(order.index(str(name)) + 1, f"{new_name}_sin")
                    order.insert(order.index(str(name)) + 2, f"{new_name}_cos")

            # Drop the original column
            if self.drop_columns or self.from_index:
                order.remove(str(name))

        return self._convert(merge(X_new, Xt)[order])


@beartype
class FeatureGenerator(TransformerMixin):
    r"""Generate new features.

    Create new combinations of existing features to capture the
    non-linear relations between the original features.

    This class can be accessed from atom through the [feature_generation]
    [atomclassifier-feature_generation] method. Read more in the
    [user guide][generating-new-features].

    !!! warning
        * Using the `div`, `log` or `sqrt` operators can return new
          features with `inf` or `NaN` values. Check the warnings that
          may pop up or use atom's [nans][atomclassifier-nans] attribute.
        * When using dfs with `n_jobs>1`, make sure to protect your code
          with `if __name__ == "__main__"`. Featuretools uses
          [dask](https://dask.org/), which uses python multiprocessing
          for parallelization. The spawn method on multiprocessing
          starts a new python process, which requires it to import the
          \__main__ module before it can do its task.
        * gfg can be slow for very large populations.

    !!! tip
        dfs can create many new features and not all of them will be
        useful. Use the [FeatureSelector][] class to reduce the number
        of features.

    Parameters
    ----------
    strategy: str, default="dfs"
        Strategy to crate new features. Choose from:

        - "[dfs][]": Deep Feature Synthesis.
        - "[gfg][]": Genetic Feature Generation.

    n_features: int or None, default=None
        Maximum number of newly generated features to add to the
        dataset. If None, select all created features.

    operators: str, sequence or None, default=None
        Mathematical operators to apply on the features. None to use
        all. Choose from: `add`, `sub`, `mul`, `div`, `abs`, `sqrt`,
        `log`, `inv`, `sin`, `cos`, `tan`.

    n_jobs: int, default=1
        Number of cores to use for parallel processing.

        - If >0: Number of cores to use.
        - If -1: Use all available cores.
        - If <-1: Use number of cores - 1 + `n_jobs`.

    verbose: int, default=0
        Verbosity level of the class. Choose from:

        - 0 to not print anything.
        - 1 to print basic information.
        - 2 to print detailed information.

    random_state: int or None, default=None
        Seed used by the random number generator. If None, the random
        number generator is the `RandomState` used by `np.random`.

    **kwargs
        Additional keyword arguments for the SymbolicTransformer
        instance. Only for the gfg strategy.

    Attributes
    ----------
    gfg_: [SymbolicTransformer][]
        Object used to calculate the genetic features. Only available
        when strategy="gfg".

    genetic_features_: pd.DataFrame
        Information on the newly created non-linear features. Only
        available when strategy="gfg". Columns include:

        - **name:** Name of the feature (generated automatically).
        - **description:** Operators used to create this feature.
        - **fitness:** Fitness score.

    feature_names_in_: np.ndarray
        Names of features seen during `fit`.

    n_features_in_: int
        Number of features seen during `fit`.

    See Also
    --------
    atom.feature_engineering:FeatureExtractor
    atom.feature_engineering:FeatureGrouper
    atom.feature_engineering:FeatureSelector

    Examples
    --------
    === "atom"
        ```pycon
        from atom import ATOMClassifier
        from sklearn.datasets import load_breast_cancer

        X, y = load_breast_cancer(return_X_y=True, as_frame=True)

        atom = ATOMClassifier(X, y)
        atom.feature_generation(strategy="dfs", n_features=5, verbose=2)

        # Note the texture error / worst symmetry column
        print(atom.dataset)
        ```

    === "stand-alone"
        ```pycon
        from atom.feature_engineering import FeatureGenerator
        from sklearn.datasets import load_breast_cancer

        X, y = load_breast_cancer(return_X_y=True, as_frame=True)

        fg = FeatureGenerator(strategy="dfs", n_features=5, verbose=2)
        X = fg.fit_transform(X, y)

        # Note the radius error * worst smoothness column
        print(X)
        ```

    """

    def __init__(
        self,
        strategy: Literal["dfs", "gfg"] = "dfs",
        *,
        n_features: IntLargerZero | None = None,
        operators: Operators | Sequence[Operators] | None = None,
        n_jobs: NJobs = 1,
        verbose: Verbose = 0,
        random_state: IntLargerEqualZero | None = None,
        **kwargs,
    ):
        super().__init__(n_jobs=n_jobs, verbose=verbose, random_state=random_state)
        self.strategy = strategy
        self.n_features = n_features
        self.operators = operators
        self.kwargs = kwargs

    def fit(self, X: XConstructor, y: YConstructor | None = None) -> Self:
        """Fit to data.

        Parameters
        ----------
        X: dataframe-like
            Feature set with shape=(n_samples, n_features).

        y: sequence, dataframe-like or None, default=None
            Target column(s) corresponding to `X`.

        Returns
        -------
        self
            Estimator instance.

        """
        Xt = to_df(X)
        yt = to_tabular(y, index=Xt.index)

        self._check_feature_names(Xt, reset=True)
        self._check_n_features(Xt, reset=True)

        all_operators = {
            "add": "add_numeric",
            "sub": "subtract_numeric",
            "mul": "multiply_numeric",
            "div": "divide_numeric",
            "abs": "absolute",
            "sqrt": "square_root",
            "log": "natural_logarithm",
            "sin": "sine",
            "cos": "cosine",
            "tan": "tangent",
        }

        if not self.operators:  # None or empty list
            operators = list(all_operators)
        else:
            operators = lst(self.operators)

        self._log("Fitting FeatureGenerator...", 1)

        if self.strategy == "dfs":
            # Run deep feature synthesis with transformation primitives
            es = ft.EntitySet(dataframes={"X": (Xt, "_index", None, None, None, True)})
            self._dfs = ft.dfs(
                target_dataframe_name="X",
                entityset=es,
                trans_primitives=[all_operators[x] for x in operators],
                max_depth=1,
                features_only=True,
                ignore_columns={"X": ["_index"]},
            )

            # Select the new features (dfs also returns originals)
            self._dfs = self._dfs[Xt.shape[1] - 1:]

            # Get a random selection of features
            if self.n_features and self.n_features < len(self._dfs):
                self._dfs = sample(self._dfs, int(self.n_features))

            # Order the features alphabetically
            self._dfs = sorted(self._dfs, key=lambda x: x._name)

        else:
            kwargs = self.kwargs.copy()  # Copy in case of repeated fit
            hall_of_fame = kwargs.pop("hall_of_fame", max(400, self.n_features or 400))
            self.gfg_ = SymbolicTransformer(
                population_size=kwargs.pop("population_size", 2000),
                hall_of_fame=hall_of_fame,
                n_components=hall_of_fame,
                init_depth=kwargs.pop("init_depth", (1, 2)),
                const_range=kwargs.pop("const_range", None),
                function_set=operators,
                feature_names=Xt.columns,
                verbose=kwargs.pop("verbose", 0 if self.verbose < 2 else 1),
                n_jobs=kwargs.pop("n_jobs", self.n_jobs),
                random_state=kwargs.pop("random_state", self.random_state),
                **kwargs,
            ).fit(Xt, yt)

        return self

    def transform(self, X: XConstructor, y: YConstructor | None = None) -> XReturn:
        """Generate new features.

        Parameters
        ----------
        X: dataframe-like
            Feature set with shape=(n_samples, n_features).

        y: sequence, dataframe-like or None, default=None
            Do nothing. Implemented for continuity of the API.

        Returns
        -------
        dataframe
            Transformed feature set.

        """
        check_is_fitted(self)

        Xt = to_df(X, columns=self.feature_names_in_)

        self._log("Generating new features...", 1)

        if self.strategy == "dfs":
            es = ft.EntitySet(dataframes={"X": (Xt, "index", None, None, None, True)})
            dfs = ft.calculate_feature_matrix(self._dfs, entityset=es, n_jobs=self.n_jobs)

            # Add the new features to the feature set
            Xt = pd.concat([Xt, dfs], axis=1).set_index("index")

            self._log(f" --> {len(self._dfs)} new features were added.", 2)

        else:
            # Get the names and fitness of the new features
            df = pd.DataFrame(
                data=[
                    ["", str(fx), fx.fitness_]
                    for i, fx in enumerate(self.gfg_)
                    if str(fx) not in Xt.columns
                ],
                columns=["name", "description", "fitness"],
            )

            # Check if any new features remain
            if len(df) == 0:
                self._log(" --> The genetic algorithm didn't find any improving features.", 2)
                return Xt

            # Select the n_features with the highest fitness
            df = df.drop_duplicates()
            df = df.nlargest(int(self.n_features or len(df)), columns="fitness")

            # If there are not enough features remaining, notify the user
            if len(df) != self.n_features:
                self._log(
                    f" --> Dropping {(self.n_features or len(self.gfg_)) - len(df)} "
                    "features due to repetition.", 2,
                )

            for i, array in enumerate(self.gfg_.transform(Xt)[:, df.index].T):
                # If the column is new, use a default name
                counter = 0
                while True:
                    name = f"x{Xt.shape[1] + counter}"
                    if name not in Xt:
                        Xt[name] = array  # Add new feature to X
                        df.iloc[i, 0] = name
                        break
                    else:
                        counter += 1

            self._log(f" --> {len(df)} new features were added.", 2)
            self.genetic_features_ = df.reset_index(drop=True)

        return self._convert(Xt)


@beartype
class FeatureGrouper(TransformerMixin):
    """Extract statistics from similar features.

    Replace groups of features with related characteristics with new
    features that summarize statistical properties of the group. The
    statistical operators are calculated over every row of the group.
    The group names and features can be accessed through the `groups`
    method.

    This class can be accessed from atom through the [feature_grouping]
    [atomclassifier-feature_grouping] method. Read more in the
    [user guide][grouping-similar-features].

    Parameters
    ----------
    groups: dict
        Group names and [features][row-and-column-selection]. A feature
        can belong to multiple groups.

    operators: str, sequence or None, default=None
        Statistical operators to apply on the groups. Any operator from
        `numpy` or `scipy.stats` (checked in that order) that is applied
        on an array can be used. If None, it uses: `min`, `max`, `mean`,
        `median`, `mode` and `std`.

    drop_columns: bool, default=True
        Whether to drop the columns in `groups` after transformation.

    verbose: int, default=0
        Verbosity level of the class. Choose from:

        - 0 to not print anything.
        - 1 to print basic information.
        - 2 to print detailed information.

    Attributes
    ----------
    feature_names_in_: np.ndarray
        Names of features seen during `fit`.

    n_features_in_: int
        Number of features seen during `fit`.

    See Also
    --------
    atom.feature_engineering:FeatureExtractor
    atom.feature_engineering:FeatureGenerator
    atom.feature_engineering:FeatureSelector

    Examples
    --------
    === "atom"
        ```pycon
        from atom import ATOMClassifier
        from sklearn.datasets import load_breast_cancer

        X, y = load_breast_cancer(return_X_y=True, as_frame=True)

        atom = ATOMClassifier(X, y)
        atom.feature_grouping({"group1": "mean.*"}, verbose=2)

        print(atom.dataset)
        ```

    === "stand-alone"
        ```pycon
        from atom.feature_engineering import FeatureGrouper
        from sklearn.datasets import load_breast_cancer

        X, _ = load_breast_cancer(return_X_y=True, as_frame=True)

        fg = FeatureGrouper({"group1": ["mean texture", "mean radius"]}, verbose=2)
        X = fg.transform(X)

        print(X)
        ```

    """

    def __init__(
        self,
        groups: dict[str, list[str]],
        *,
        operators: str | Sequence[str] | None = None,
        drop_columns: Bool = True,
        verbose: Verbose = 0,
    ):
        super().__init__(verbose=verbose)
        self.groups = groups
        self.operators = operators
        self.drop_columns = drop_columns

    def transform(self, X: XConstructor, y: YConstructor | None = None) -> XReturn:
        """Group features.

        Parameters
        ----------
        X: dataframe-like
            Feature set with shape=(n_samples, n_features).

        y: sequence, dataframe-like or None, default=None
            Do nothing. Implemented for continuity of the API.

        Returns
        -------
        dataframe
            Transformed feature set.

        """
        Xt = to_df(X, columns=getattr(self, "feature_names_in_", None))

        self._log("Grouping features...", 1)

        if self.operators is None:
            operators = ["min", "max", "mean", "median", "mode", "std"]
        else:
            operators = lst(self.operators)

        to_drop = []
        for name, group in self.groups.items():
            for operator in operators:
                try:
                    result = Xt[group].apply(getattr(np, operator), axis=1)
                except AttributeError:
                    try:
                        result = getattr(stats, operator)(Xt[group], axis=1)[0]
                    except AttributeError:
                        raise ValueError(
                            "Invalid value for the operators parameter. Value "
                            f"{operator} is not an attribute of numpy nor scipy.stats."
                        ) from None

                try:
                    Xt[f"{operator}({name})"] = result
                except ValueError:
                    raise ValueError(
                        "Invalid value for the operators parameter. Value "
                        f"{operator} doesn't return a one-dimensional array."
                    ) from None

            to_drop.extend(group)
            self._log(f" --> Group {name} successfully created.", 2)

        if self.drop_columns:
            Xt = Xt.drop(columns=to_drop)

        return self._convert(Xt)


@beartype
class FeatureSelector(TransformerMixin):
    """Reduce the number of features in the data.

    Apply feature selection or dimensionality reduction, either to
    improve the estimators' accuracy or to boost their performance on
    very high-dimensional datasets. Additionally, remove multicollinear
    and low-variance features.

    This class can be accessed from atom through the [feature_selection]
    [atomclassifier-feature_selection] method. Read more in the
    [user guide][selecting-useful-features].

    !!! warning
        - Ties between features with equal scores are broken in an
          unspecified way.
        - For strategy="rfecv", the `n_features` parameter is the
          **minimum** number of features to select, not the actual
          number of features that the transformer returns. It may very
          well be that it returns more!

    !!! info
        - The "sklearnex" and "cuml" engines are only supported for
          strategy="pca" with dense datasets.
        - If strategy="pca" and the data is dense and unscaled, it's
          scaled to mean=0 and std=1 before fitting the PCA transformer.
        - If strategy="pca" and the provided data is sparse, the used
          estimator is [TruncatedSVD][], which works more efficiently
          with sparse matrices.

    !!! tip
        * Use the [plot_pca][] and [plot_components][] methods to
          examine the results after using strategy="pca".
        * Use the [plot_rfecv][] method to examine the results after
          using strategy="rfecv".
        * Use the [plot_feature_importance][] method to examine how
          much a specific feature contributes to the final predictions.
          If the model doesn't have a `feature_importances_` attribute,
          use [plot_permutation_importance][] instead.

    Parameters
    ----------
    strategy: str or None, default=None
        Feature selection strategy to use. Choose from:

        - None: Do not perform any feature selection strategy.
        - "[univariate][selectkbest]": Univariate statistical F-test.
        - "[pca][]": Principal Component Analysis.
        - "[sfm][]": Select best features according to a model.
        - "[sfs][]": Sequential Feature Selection.
        - "[rfe][]": Recursive Feature Elimination.
        - "[rfecv][]": RFE with cross-validated selection.
        - "[pso][]": Particle Swarm Optimization.
        - "[hho][]": Harris Hawks Optimization.
        - "[gwo][]": Grey Wolf Optimization.
        - "[dfo][]": Dragonfly Optimization.
        - "[go][]": Genetic Optimization.

    solver: str, func, predictor or None, default=None
        Solver/estimator to use for the feature selection strategy. See
        the corresponding documentation for an extended description of
        the choices. If None, the default value is used (only if
        strategy="pca"). Choose from:

        - If strategy="univariate":

            - "[f_classif][]"
            - "[f_regression][]"
            - "[mutual_info_classif][]"
            - "[mutual_info_regression][]"
            - "[chi2][]"
            - Any function with signature `func(X, y) -> tuple[scores, p-values]`.

        - If strategy="pca":

            - If data is dense:

                - If engine="sklearn":

                    - "auto" (default)
                    - "full"
                    - "covariance_eigh"
                    - "arpack"
                    - "randomized"

                - If engine="sklearnex":

                    - "full" (default)

                - If engine="cuml":

                    - "full" (default)
                    - "jacobi"

            - If data is sparse:

                - "randomized" (default)
                - "covariance_eigh"
                - "arpack"

        - for the remaining strategies:<br>
          The base estimator. For sfm, rfe and rfecv, it should have
          either a `feature_importances_` or `coef_` attribute after
          fitting. You can use one of the [predefined models][]. Add
          `_class` or `_reg` after the model's  name to specify a
          classification or regression task, e.g., `solver="LGB_reg"`
          (not necessary if called from atom). No default option.

    n_features: int, float or None, default=None
        Number of features to select.

        - If None: Select all features.
        - If <1: Fraction of the total features to select.
        - If >=1: Number of features to select.

        If strategy="sfm" and the threshold parameter is not specified,
        the threshold is automatically set to `-inf` to select
        `n_features` number of features.

        If strategy="rfecv", `n_features` is the minimum number of
        features to select.

        This parameter is ignored if any of the following strategies
        is selected: pso, hho, gwo, dfo, go.

    min_repeated: int, float or None, default=2
        Remove categorical features if there isn't any repeated value
        in at least `min_repeated` rows. The default is to keep all
        features with non-maximum variance, i.e., remove the features
        which number of unique values is equal to the number of rows
        (usually the case for names, IDs, etc...).

        - If None: No check for minimum repetition.
        - If >1: Minimum repetition number.
        - If <=1: Minimum repetition fraction.

    max_repeated: int, float or None, default=1.0
        Remove categorical features with the same value in at least
        `max_repeated` rows. The default is to keep all features with
        non-zero variance, i.e., remove the features that have the same
        value in all samples.

        - If None: No check for maximum repetition.
        - If >1: Maximum number of repeated occurences.
        - If <=1: Maximum fraction of repeated occurences.

    max_correlation: float or None, default=1.0
        Minimum absolute [Pearson correlation][pearson] to identify
        correlated features. For each group, it removes all except the
        feature with the highest correlation to `y` (if provided, else
        it removes all but the first). The default value removes equal
        columns. If None, skip this step.

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

    engine: str or None, default=None
        Execution engine to use for [estimators][estimator-acceleration].
        If None, the default value is used. Choose from:

        - "sklearn" (default)
        - "cuml"

    verbose: int, default=0
        Verbosity level of the class. Choose from:

        - 0 to not print anything.
        - 1 to print basic information.
        - 2 to print detailed information.

    random_state: int or None, default=None
        Seed used by the random number generator. If None, the random
        number generator is the `RandomState` used by `np.random`.

    **kwargs
        Any extra keyword argument for the `strategy` estimator. See the
        corresponding documentation for the available options.

    Attributes
    ----------
    collinear_: pd.DataFrame
        Information on the removed collinear features. Columns include:

        - **drop:** Name of the dropped feature.
        - **corr_feature:** Names of the correlated features.
        - **corr_value:** Corresponding correlation coefficients.

    [strategy]_: sklearn transformer
        Object used to transform the data, e.g., `fs.pca` for the pca
        strategy.

    feature_names_in_: np.ndarray
        Names of features seen during `fit`.

    n_features_in_: int
        Number of features seen during `fit`.

    See Also
    --------
    atom.feature_engineering:FeatureExtractor
    atom.feature_engineering:FeatureGenerator
    atom.feature_engineering:FeatureGrouper

    Examples
    --------
    === "atom"
        ```pycon
        from atom import ATOMClassifier
        from sklearn.datasets import load_breast_cancer

        X, y = load_breast_cancer(return_X_y=True, as_frame=True)

        atom = ATOMClassifier(X, y)
        atom.feature_selection(strategy="pca", n_features=12, verbose=2)

        # Note that the column names changed
        print(atom.dataset)
        ```

    === "stand-alone"
        ```pycon
        from atom.feature_engineering import FeatureSelector
        from sklearn.datasets import load_breast_cancer

        X, _ = load_breast_cancer(return_X_y=True, as_frame=True)

        fs = FeatureSelector(strategy="pca", n_features=12, verbose=2)
        X = fs.fit_transform(X)

        # Note that the column names changed
        print(X)
        ```

    """

    def __init__(
        self,
        strategy: FeatureSelectionStrats | None = None,
        *,
        solver: FeatureSelectionSolvers = None,
        n_features: FloatLargerZero | None = None,
        min_repeated: FloatLargerEqualZero | None = 2,
        max_repeated: FloatLargerEqualZero | None = 1.0,
        max_correlation: FloatZeroToOneInc | None = 1.0,
        n_jobs: NJobs = 1,
        device: str = "cpu",
        engine: Engine = None,
        verbose: Verbose = 0,
        random_state: IntLargerEqualZero | None = None,
        **kwargs,
    ):
        super().__init__(
            n_jobs=n_jobs,
            device=device,
            engine=engine,
            verbose=verbose,
            random_state=random_state,
        )
        self.strategy = strategy
        self.solver = solver
        self.n_features = n_features
        self.min_repeated = min_repeated
        self.max_repeated = max_repeated
        self.max_correlation = max_correlation
        self.kwargs = kwargs

    def fit(self, X: XConstructor, y: YConstructor | None = None) -> Self:
        """Fit the feature selector to the data.

        The univariate, sfm (when model is not fitted), sfs, rfe and
        rfecv strategies need a target column. Leaving it None raises
        an exception.

        Parameters
        ----------
        X: dataframe-like
            Feature set with shape=(n_samples, n_features).

        y: sequence, dataframe-like or None, default=None
            Target column(s) corresponding to `X`.

        Returns
        -------
        self
            Estimator instance.

        """
        from atom.models import MODELS

        def objective_function(model, X_train, y_train, X_valid, y_valid, scoring):
            """Objective function for the advanced optimization strategies."""
            if X_train.equals(X_valid):
                cv = cross_val_score(model, X_train, y_train, cv=3, scoring=scoring)
                return np.mean(cv, axis=0)
            else:
                model.fit(X_train, y_train)
                return scoring(model, X_valid, y_valid)

        Xt = to_df(X)
        yt = to_tabular(y, index=Xt.index)

        if yt is None and self.strategy not in ("pca", "sfm", None):
            raise ValueError(
                "Invalid value for the y parameter. Value cannot "
                f"be None for strategy='{self.strategy}'."
            )

        self._check_feature_names(Xt, reset=True)
        self._check_n_features(Xt, reset=True)

        self.collinear_ = pd.DataFrame(columns=["drop", "corr_feature", "corr_value"])
        self.scaler_ = None

        kwargs = self.kwargs.copy()
        self._high_variance: dict[Hashable, tuple[Hashable, int]] = {}
        self._low_variance: dict[Hashable, tuple[Hashable, float]] = {}
        self._estimator: Any = None
        self._n_features: int | None = None

        if isinstance(self.strategy, str):
            if self.strategy not in ("univariate", "pca"):
                solver: FeatureSelectionSolvers

                if self.solver is None:
                    raise ValueError(
                        "Invalid value for the solver parameter. The "
                        f"value can't be None for strategy={self.strategy}"
                    )
                elif isinstance(self.solver, str):
                    # Assign goal to initialize the predefined model
                    if self.solver[-6:] == "_class":
                        goal = Goal.classification
                        solver = self.solver[:-6]
                    elif self.solver[-4:] == "_reg":
                        goal = Goal.regression
                        solver = self.solver[:-4]
                    else:
                        raise ValueError(
                            "Invalid value for the solver parameter. The name of the model "
                            "must be followed by '_class' or '_reg' to specify the task, e.g.,"
                            "solver='RF_class'."
                        )

                    # Get estimator from predefined models
                    if solver in MODELS:
                        model = MODELS[solver](
                            goal=goal,
                            **{
                                x: getattr(self, x)
                                for x in BaseTransformer.attrs
                                if hasattr(self, x)
                            },
                        )
                        if yt is not None:
                            model.task = goal.infer_task(yt)
                        solver = model._get_est({})
                    else:
                        raise ValueError(
                            "Invalid value for the solver parameter. Unknown "
                            f"model: {solver}. Available models are:\n" +
                            "\n".join(
                                [
                                    f" --> {m.__name__} ({m.acronym})"
                                    for m in MODELS
                                    if goal.name in m._estimators
                                ]
                            )
                        )
                elif callable(self.solver):
                    solver = self._inherit(self.solver())  # type: ignore[type-var, assignment]
                else:
                    solver = self.solver

        elif self.kwargs:
            kw = ", ".join([f"{k}={v}" for k, v in self.kwargs.items()])
            raise ValueError(
                f"Keyword arguments ({kw}) are specified for "
                "the strategy estimator but no strategy is selected."
            )

        if self.n_features is None:
            self._n_features = Xt.shape[1]
        elif self.n_features < 1:
            self._n_features = int(self.n_features * Xt.shape[1])
        else:
            self._n_features = int(self.n_features)

        min_repeated: Scalar
        if self.min_repeated is None:
            min_repeated = 1
        elif self.min_repeated <= 1:
            min_repeated = self.min_repeated * len(Xt)
        else:
            min_repeated = int(self.min_repeated)

        max_repeated: Scalar
        if self.max_repeated is None:
            max_repeated = len(Xt)
        elif self.max_repeated <= 1:
            max_repeated = self.max_repeated * len(Xt)
        else:
            max_repeated = int(self.max_repeated)

        if min_repeated > max_repeated:
            raise ValueError(
                "The min_repeated parameter can't be higher than "
                f"max_repeated, got {min_repeated} > {max_repeated}. "
            )

        self._log("Fitting FeatureSelector...", 1)

        # Remove features with too high variance
        if self.min_repeated is not None:
            for name, column in Xt.select_dtypes(exclude="number").items():
                max_counts = column.value_counts()
                if min_repeated > max_counts.max():
                    self._high_variance[name] = (max_counts.idxmax(), max_counts.max())
                    Xt = Xt.drop(columns=name)
                    break

        # Remove features with too low variance
        if self.max_repeated is not None:
            for name, column in Xt.select_dtypes(exclude="number").items():
                for category, count in column.value_counts().items():
                    if count >= max_repeated:
                        self._low_variance[name] = (category, 100.0 * count / len(Xt))
                        Xt = Xt.drop(columns=name)
                        break

        # Remove features with too high correlation
        self.collinear = pd.DataFrame(columns=["drop", "corr_feature", "corr_value"])
        if self.max_correlation:
            # Get the Pearson correlation coefficient matrix
            if yt is None:
                corr_X = Xt.corr()
            else:
                corr_matrix = merge(Xt, yt).corr()
                corr_X, corr_y = corr_matrix.iloc[:-1, :-1], corr_matrix.iloc[:-1, -1]

            corr = {}
            to_drop = []
            for col in corr_X:
                # Select columns that are corr
                corr[col] = corr_X[col][corr_X[col] >= self.max_correlation]

                # Always finds himself with correlation 1
                if len(corr[col]) > 1:
                    if yt is None:
                        # Drop all but the first one
                        to_drop.extend(list(corr[col][1:].index))
                    else:
                        # Keep feature with the highest correlation with y
                        keep = corr_y[corr[col].index].idxmax()
                        to_drop.extend(list(corr[col].index.drop(keep)))

            for col in list(dict.fromkeys(to_drop)):
                corr_feature = corr[col].drop(col).index
                corr_value = corr[col].drop(col).round(4).astype(str)
                self.collinear_ = pd.concat(
                    [
                        self.collinear_,
                        pd.DataFrame(
                            {
                                "drop": [col],
                                "corr_feature": [", ".join(corr_feature)],
                                "corr_value": [", ".join(corr_value)],
                            }
                        ),
                    ],
                    ignore_index=True,
                )

            Xt = Xt.drop(columns=self.collinear_["drop"].tolist())

        if self.strategy is None:
            return self  # Exit feature_engineering

        elif self.strategy == "univariate":
            solvers_dct = {
                "f_classif": f_classif,
                "f_regression": f_regression,
                "mutual_info_classif": mutual_info_classif,
                "mutual_info_regression": mutual_info_regression,
                "chi2": chi2,
            }

            if not self.solver:
                raise ValueError(
                    "Invalid value for the solver parameter. The "
                    f"value can't be None for strategy={self.strategy}"
                )
            elif isinstance(self.solver, str):
                if self.solver in solvers_dct:
                    solver = solvers_dct[self.solver]
                else:
                    raise ValueError(
                        "Invalid value for the solver parameter, got "
                        f"{self.solver}. Choose from: {', '.join(solvers_dct)}."
                    )
            else:
                solver = self.solver

            self._estimator = SelectKBest(solver, k=self._n_features).fit(Xt, yt)

        elif self.strategy == "pca":
            if not is_sparse(Xt):
                # PCA requires the features to be scaled
                if not check_scaling(Xt):
                    self.scaler_ = Scaler(device=self.device, engine=self.engine)
                    Xt = cast(pd.DataFrame, self.scaler_.fit_transform(Xt))

                estimator = self._get_est_class("PCA", "decomposition")
                solver_param = "svd_solver"
            else:
                estimator = self._get_est_class("TruncatedSVD", "decomposition")
                solver_param = "algorithm"

            if self.solver is None:
                solver = sign(estimator)[solver_param].default
            else:
                solver = self.solver

            # The PCA and TruncatedSVD both get all possible components to use
            # for the plots (n_components must be < n_features and <= n_rows)
            self._estimator = estimator(
                n_components=min(len(Xt), Xt.shape[1] - 1),
                **{solver_param: solver},
                random_state=self.random_state,
                **self.kwargs,
            ).fit(Xt)

            self._estimator._comps = min(self._estimator.components_.shape[0], self._n_features)

        elif self.strategy == "sfm":
            # If any of these attr exists, the model is already fitted
            if any(hasattr(solver, a) for a in ("coef_", "feature_importances_")):
                prefit = kwargs.pop("prefit", True)
            else:
                prefit = False

            # If a threshold is not specified, select only based on _n_features
            if not self.kwargs.get("threshold"):
                kwargs["threshold"] = -np.inf

            self._estimator = SelectFromModel(
                estimator=solver,
                max_features=self._n_features,
                prefit=prefit,
                **kwargs,
            )
            if prefit:
                if list(getattr(solver, "feature_names_in_", [])) != list(Xt.columns):
                    raise ValueError(
                        "Invalid value for the solver parameter. The "
                        f"{solver.__class__.__name__} estimator "
                        "is fitted using different columns than X!"
                    )
                self._estimator.estimator_ = solver
            else:
                self._estimator.fit(Xt, yt)

        elif self.strategy in ("sfs", "rfe", "rfecv"):
            if self.strategy == "sfs":
                if self.kwargs.get("scoring"):
                    kwargs["scoring"] = get_custom_scorer(self.kwargs["scoring"])

                self._estimator = SequentialFeatureSelector(
                    estimator=solver,
                    n_features_to_select=self._n_features,
                    n_jobs=self.n_jobs,
                    **kwargs,
                )

            elif self.strategy == "rfe":
                self._estimator = RFE(
                    estimator=solver,
                    n_features_to_select=self._n_features,
                    **kwargs,
                )

            elif self.strategy == "rfecv":
                if self.kwargs.get("scoring"):
                    kwargs["scoring"] = get_custom_scorer(self.kwargs["scoring"])

                # Invert n_features to select them all (default option)
                if self._n_features == Xt.shape[1]:
                    self._n_features = 1

                self._estimator = RFECV(
                    estimator=solver,
                    min_features_to_select=self._n_features,
                    n_jobs=self.n_jobs,
                    **kwargs,
                )

            self._estimator.fit(Xt, yt)

        else:
            strategies = {
                "pso": ParticleSwarmOptimization,
                "hho": HarrisHawkOptimization,
                "gwo": GreyWolfOptimization,
                "dfo": DragonFlyOptimization,
                "go": GeneticOptimization,
            }

            # Either use a provided validation set or cross-validation over X
            if "X_valid" in kwargs:
                if "y_valid" in kwargs:
                    X_valid, y_valid = self._check_input(
                        kwargs.pop("X_valid"), kwargs.pop("y_valid")
                    )
                else:
                    raise ValueError(
                        "Invalid value for the y_valid parameter. The value "
                        "cannot be absent when X_valid is provided."
                    )
            else:
                X_valid, y_valid = Xt, yt

            # Get scoring for default objective_function
            if "objective_function" not in kwargs:
                if kwargs.get("scoring"):
                    kwargs["scoring"] = get_custom_scorer(kwargs["scoring"])
                else:
                    goal = Goal(0) if is_classifier(solver) else Goal(1)
                    if yt is not None:
                        task = goal.infer_task(yt)
                    if task is Task.binary_classification:
                        kwargs["scoring"] = get_custom_scorer("f1")
                    elif task.is_multiclass:
                        kwargs["scoring"] = get_custom_scorer("f1_weighted")
                    else:
                        kwargs["scoring"] = get_custom_scorer("r2")

            self._estimator = strategies[self.strategy](
                objective_function=kwargs.pop("objective_function", objective_function),
                minimize=kwargs.pop("minimize", False),
                **kwargs,
            )

            self._estimator.fit(
                model=solver,
                X_train=Xt,
                y_train=yt,
                X_valid=X_valid,
                y_valid=y_valid,
                verbose=self.verbose >= 2,
            )

        # Add the strategy estimator as attribute to the class
        setattr(self, f"{self.strategy}_", self._estimator)

        return self

    def get_feature_names_out(self, input_features: Sequence[str] | None = None) -> np.ndarray:
        """Get output feature names for transformation.

        Parameters
        ----------
        input_features: sequence or None, default=None
            Only used to validate feature names with the names seen in
            `fit`.

        Returns
        -------
        np.ndarray
            Transformed feature names.

        """
        check_is_fitted(self, attributes="feature_names_in_")
        _check_feature_names_in(self, input_features)

        if self._estimator:
            if hasattr(self._estimator, "get_feature_names_out"):
                if self.strategy == "rfecv":
                    return self._estimator.get_feature_names_out()
                else:
                    # _n_features is the minimum number of features with rfecv
                    return self._estimator.get_feature_names_out()[:self._n_features]
            else:
                raise NotImplementedError(
                    "The get_feature_names_out method is not implemented "
                    f"for any of the advanced strategies, got {self.strategy}. "
                    "Use a sklearn strategy (e.g., SFS, SFM or RFE) instead."
                )
        else:
            return np.array(
                [
                    c
                    for c in self.feature_names_in_
                    if (
                        c not in self._high_variance
                        and c not in self._low_variance
                        and c not in self.collinear_["drop"].to_numpy()
                    )
                ]
            )

    def transform(self, X: XConstructor, y: YConstructor | None = None) -> XReturn:
        """Transform the data.

        Parameters
        ----------
        X: dataframe-like
            Feature set with shape=(n_samples, n_features).

        y: sequence, dataframe-like or None, default=None
            Do nothing. Implemented for continuity of the API.

        Returns
        -------
        dataframe
            Transformed feature set.

        """
        check_is_fitted(self)

        Xt = to_df(X, columns=self.feature_names_in_)

        self._log("Performing feature selection ...", 1)

        # Remove features with too high variance
        for fx, h_variance in self._high_variance.items():
            self._log(
                f" --> Feature {fx} was removed due to high variance. "
                f"Value {h_variance[0]} was the most repeated value with "
                f"{h_variance[1]} ({h_variance[1] / len(Xt):.1f}%) occurrences.", 2,
            )
            Xt = Xt.drop(columns=fx)

        # Remove features with too low variance
        for fx, l_variance in self._low_variance.items():
            self._log(
                f" --> Feature {fx} was removed due to low variance. Value "
                f"{l_variance[0]} repeated in {l_variance[1]:.1f}% of the rows.", 2,
            )
            Xt = Xt.drop(columns=fx)

        # Remove features with too high correlation
        for col in self.collinear_["drop"]:
            self._log(
                f" --> Feature {col} was removed due to "
                "collinearity with another feature.", 2,
            )
            Xt = Xt.drop(columns=col)

        # Perform selection based on strategy
        if self.strategy is None:
            return self._convert(Xt)

        elif self.strategy == "univariate":
            self._log(
                f" --> The univariate test selected "
                f"{self._n_features} features from the dataset.", 2,
            )
            for n, column in enumerate(Xt):
                if not self.univariate_.get_support()[n]:
                    self._log(
                        f"   --> Dropping feature {column} "
                        f"(score: {self.univariate_.scores_[n]:.2f}  "
                        f"p-value: {self.univariate_.pvalues_[n]:.2f}).", 2,
                    )
                    Xt = Xt.drop(columns=column)

        elif self.strategy == "pca":
            self._log(" --> Applying Principal Component Analysis...", 2)

            if self.scaler_:
                self._log("   --> Scaling features...", 2)
                Xt = cast(pd.DataFrame, self.scaler_.transform(Xt))

            Xt = self._estimator.transform(Xt).iloc[:, :self._estimator._comps]

            var = np.array(self._estimator.explained_variance_ratio_[:self._n_features])
            self._log(f"   --> Keeping {self._estimator._comps} components.", 2)
            self._log(f"   --> Explained variance ratio: {round(var.sum(), 3)}", 2)

        elif self.strategy in ("sfm", "sfs", "rfe", "rfecv"):
            mask = self._estimator.get_support()
            self._log(f" --> {self.strategy} selected {sum(mask)} features from the dataset.", 2)

            for n, column in enumerate(Xt):
                if not mask[n]:
                    if hasattr(self._estimator, "ranking_"):
                        self._log(
                            f"   --> Dropping feature {column} "
                            f"(rank {self._estimator.ranking_[n]}).", 2,
                        )
                    else:
                        self._log(f"   --> Dropping feature {column}.", 2)
                    Xt = Xt.drop(columns=column)

        else:  # Advanced strategies
            self._log(
                f" --> {self.strategy} selected {len(self._estimator.best_feature_list)} "
                "features from the dataset.", 2,
            )

            for column in Xt:
                if column not in self._estimator.best_feature_list:
                    self._log(f"   --> Dropping feature {column}.", 2)
                    Xt = Xt.drop(columns=column)

        return self._convert(Xt)
