"""Automated Tool for Optimized Modeling (ATOM).

Author: Mavs
Description: Unit tests for feature_engineering.py

"""

import pandas as pd
import pytest
from sklearn.feature_selection import f_regression
from sklearn.tree import DecisionTreeClassifier

from atom.feature_engineering import (
    FeatureExtractor, FeatureGenerator, FeatureGrouper, FeatureSelector,
)
from atom.utils.utils import to_df

from .conftest import (
    X10_dt, X10_str, X_bin, X_class, X_reg, X_sparse, y_bin, y_class, y_fc,
    y_reg,
)


# Test FeatureExtractor ============================================ >>

def test_invalid_features():
    """Assert that an error is raised when features are invalid."""
    with pytest.raises(ValueError, match=".*an attribute of pd.Series.dt.*"):
        FeatureExtractor(features="invalid").transform(X10_dt)


def test_from_index_invalid():
    """Assert that an error is raised when the index is no datetime."""
    extractor = FeatureExtractor(from_index=True)
    with pytest.raises(ValueError, match=".*index to a timestamp format.*"):
        extractor.transform(X_bin)


def test_from_index():
    """Assert that features can be extracted from the index."""
    extractor = FeatureExtractor(from_index=True)
    X = extractor.transform(pd.DataFrame(y_fc))
    assert "Period_year" in X.columns


def test_skip_no_variance():
    """Assert that features with no variance are not in the output."""
    extractor = FeatureExtractor(from_index=True)
    X = extractor.transform(pd.DataFrame(y_fc))
    assert "Period_day" not in X.columns


def test_wrongly_converted_columns_are_ignored():
    """Assert that columns converted unsuccessfully are skipped."""
    extractor = FeatureExtractor()
    X = extractor.transform(X10_str)
    assert "x2" in X.columns


def test_datetime_features_are_used():
    """Assert that datetime64 features are used as is."""
    X = to_df(X10_dt)
    X["x2"] = pd.to_datetime(X["x2"], dayfirst=True)

    extractor = FeatureExtractor(features="day")
    X = extractor.transform(X)
    assert "x2_day" in X.columns
    assert "x2" not in X.columns


def test_wrongly_converted_features_are_ignored():
    """Assert that wrongly converted features are ignored."""
    extractor = FeatureExtractor(features=["tz", "is_leap_year", "day"])
    X = extractor.transform(X10_dt)
    assert "x1_tz" not in X.columns  # Not pd.Series.dt


def test_ordinal_features():
    """Assert that ordinal features are created."""
    extractor = FeatureExtractor(features="day")
    X = extractor.transform(X10_dt)
    assert "x2_day" in X.columns
    assert "x2" not in X.columns


def test_order_features():
    """Assert that the new features are in the order provided."""
    extractor = FeatureExtractor()
    X = extractor.transform(X10_dt)
    assert X.columns.get_loc("x2_year") == 2
    assert X.columns.get_loc("x2_month") == 3
    assert X.columns.get_loc("x2_day") == 4


@pytest.mark.parametrize(
    "fxs",
    [
        ("microsecond", "%f"),
        ("second", "%S"),
        ("hour", "%H"),
        ("weekday", "%d/%m/%Y"),
        ("day", "%d/%m/%Y"),
        ("dayofyear", "%d/%m/%Y"),
        ("month", "%d/%m/%Y"),
        ("quarter", "%d/%m/%Y"),
    ],
)
def test_all_cyclic_features(fxs):
    """Assert that all cyclic columns create two features."""
    extractor = FeatureExtractor(features=fxs[0], fmt=fxs[1], encoding_type="cyclic")
    X = extractor.transform(X10_dt)
    assert any(X.columns.str.contains(f"{fxs[0]}_cos"))
    assert X.shape[1] == 4 + 1  # 2 new and og is dropped


def test_features_are_not_dropped():
    """Assert that features are kept when drop_columns=False."""
    extractor = FeatureExtractor(drop_columns=False)
    X = extractor.transform(X10_dt)
    assert "x2" in X.columns


# Test FeatureGenerator ============================================ >>

def test_n_features_above_maximum():
    """Assert that n_features becomes maximum if more than maximum."""
    generator = FeatureGenerator(
        strategy="dfs",
        n_features=1000,
        operators="log",
        random_state=1,
    )
    X = generator.fit_transform(X_bin, y_bin)
    assert X.shape[1] == 60  # 30 og + 30 log


def test_genetic_non_improving_features():
    """Assert that the code doesn't fail if there are no new improving features."""
    generator = FeatureGenerator(
        strategy="gfg",
        generations=5,
        population_size=30,
        hall_of_fame=10,
        operators="sqrt",
        random_state=1,
    )
    _ = generator.fit_transform(X_reg, y_reg)
    assert not hasattr(generator, "genetic_features_")


def test_attribute_genetic_features():
    """Assert that the genetic_features attribute is created."""
    generator = FeatureGenerator(
        strategy="gfg",
        generations=3,
        population_size=30,
        hall_of_fame=10,
        random_state=1,
    )
    _ = generator.fit_transform(X_bin, y_bin)
    assert not generator.genetic_features_.empty


def test_updated_dataset():
    """Assert that the feature set contains the new features."""
    generator = FeatureGenerator(strategy="dfs", n_features=None, random_state=1)
    X = generator.fit_transform(X_bin, y_bin)
    assert X.shape[1] > X_bin.shape[1]


def test_default_feature_names():
    """Assert that the new features get the correct default names."""
    X = X_bin.copy()
    X["x31"] = range(len(X))

    generator = FeatureGenerator(
        strategy="gfg",
        n_features=1,
        population_size=200,
        hall_of_fame=10,
        random_state=1,
    )
    X = generator.fit_transform(X, y_bin)
    assert "x32" in X
    assert "x30" not in X


# Test FeatureGrouper ============================================= >>

def test_operator_not_in_libraries():
    """Assert that an error is raised when an operator is not in np or stats."""
    grouper = FeatureGrouper({"g1": ["mean radius", "mean texture"]}, operators="invalid")
    with pytest.raises(ValueError, match=".*operators parameter.*"):
        grouper.transform(X_bin)


def test_invalid_operator():
    """Assert that an error is raised when the result is not one-dimensional."""
    grouper = FeatureGrouper({"g1": ["mean radius", "mean texture"]}, operators="log")
    with pytest.raises(ValueError, match=".*one-dimensional.*"):
        grouper.transform(X_bin)


def test_groups_are_created():
    """Assert that the groups are made."""
    grouper = FeatureGrouper({"g1": ["mean radius", "mean texture"]})
    X = grouper.transform(X_bin)
    assert "mean(g1)" in X.columns
    assert X.columns[0] != X_bin.columns[0]


def test_custom_operators():
    """Assert that custom operators can be used."""
    grouper = FeatureGrouper({"g1": ["mean radius", "mean texture"]}, operators="var")
    X = grouper.transform(X_bin)
    assert "var(g1)" in X.columns


def test_columns_are_kept():
    """Assert that group columns can be kept."""
    grouper = FeatureGrouper({"g1": ["mean radius", "mean texture"]}, drop_columns=False)
    X = grouper.transform(X_bin)
    assert X.columns[0] == X_bin.columns[0]


# Test FeatureSelector ============================================= >>

def test_solver_parameter_empty():
    """Assert that an error is raised when solver is None."""
    selector = FeatureSelector(strategy="sfm", solver=None)
    with pytest.raises(ValueError, match=".*can't be None.*"):
        selector.fit(X_reg, y_reg)


def test_goal_attribute():
    """Assert that the goal is deduced from the model's name."""
    # For classification tasks
    selector = FeatureSelector(strategy="sfm", solver="LGB_class")
    selector.fit(X_bin, y_bin)
    assert selector._estimator.estimator.__class__.__name__.endswith("Classifier")

    # For regression tasks
    selector = FeatureSelector(strategy="sfm", solver="LGB_reg")
    selector.fit(X_reg, y_reg)
    assert selector._estimator.estimator.__class__.__name__.endswith("Regressor")


def test_sfm_invalid_solver():
    """Assert that an error is raised when solver is invalid."""
    selector = FeatureSelector(strategy="sfm", solver="invalid_class", n_features=5)
    with pytest.raises(ValueError, match=".*Unknown model.*"):
        selector.fit_transform(X_bin, y_bin)


def test_sfm_invalid_solver_no_task():
    """Assert that an error is raised when solver is invalid."""
    selector = FeatureSelector(strategy="sfm", solver="RF")
    with pytest.raises(ValueError, match=".*must be followed by '_class'.*"):
        selector.fit_transform(X_bin, y_bin)


def test_kwargs_but_no_strategy():
    """Assert that an error is raised when kwargs are defined and strategy=None."""
    selector = FeatureSelector(strategy=None, cv=2)
    with pytest.raises(ValueError, match=".*Keyword arguments.*"):
        selector.fit(X_reg, y_reg)


def test_max_repeated_smaller_min_repeated():
    """Assert that an error is raised when min_repeated > max_repeated."""
    selector = FeatureSelector(strategy=None, min_repeated=100, max_repeated=2)
    with pytest.raises(ValueError, match=".*can't be higher.*"):
        selector.fit(X_reg, y_reg)


def test_error_y_is_None():
    """Assert that an error is raised when y is None for some strategies."""
    selector = FeatureSelector(strategy="univariate", solver=f_regression, n_features=9)
    with pytest.raises(ValueError, match=".*the y parameter.*"):
        selector.fit(X_reg)


@pytest.mark.parametrize("min_repeated", [2, 0.1])
def test_remove_high_variance(min_repeated):
    """Assert that high-variance features are removed."""
    X = X_bin.copy()
    X["invalid"] = [f"{i}" for i in range(len(X))]  # Add column with maximum variance
    selector = FeatureSelector(min_repeated=min_repeated, max_repeated=None)
    X = selector.fit_transform(X)
    assert X.shape[1] == X_bin.shape[1]
    assert list(selector.get_feature_names_out()) == list(X.columns)


@pytest.mark.parametrize("max_repeated", [400, 0.9])
def test_remove_low_variance(max_repeated):
    """Assert that low-variance features are removed."""
    X = X_bin.copy()
    X["invalid"] = "test"  # Add column with minimum variance
    selector = FeatureSelector(min_repeated=None, max_repeated=max_repeated)
    X = selector.fit_transform(X)
    assert X.shape[1] == X_bin.shape[1]
    assert list(selector.get_feature_names_out()) == list(X.columns)


def test_remove_collinear_without_y():
    """Assert that the remove_collinear function works when y is provided."""
    X = X_bin.copy()
    X["valid"] = list(range(len(X)))
    X["invalid"] = list(range(len(X)))
    selector = FeatureSelector(max_correlation=1)
    X = selector.fit_transform(X)
    assert "valid" in X
    assert "invalid" not in X
    assert hasattr(selector, "collinear_")
    assert list(selector.get_feature_names_out()) == list(X.columns)


def test_remove_collinear_with_y():
    """Assert that the remove_collinear function works when y is not provided."""
    selector = FeatureSelector(max_correlation=0.9)
    X = selector.fit_transform(X_bin, y_bin)
    assert X.shape[1] < X_bin.shape[1]
    assert hasattr(selector, "collinear_")
    assert list(selector.get_feature_names_out()) == list(X.columns)


def test_solver_parameter_empty_univariate():
    """Assert that an error is raised when solver is None for univariate."""
    selector = FeatureSelector(strategy="univariate")
    with pytest.raises(ValueError, match=".*can't be None.*"):
        selector.fit(X_reg, y_reg)


def test_raise_unknown_solver_univariate():
    """Assert that an error is raised when the solver is unknown."""
    selector = FeatureSelector(strategy="univariate", solver="invalid")
    with pytest.raises(ValueError, match=".*the solver parameter.*"):
        selector.fit(X_reg, y_reg)


def test_univariate_strategy_custom_solver():
    """Assert that the univariate strategy works for a custom solver."""
    selector = FeatureSelector("univariate", solver=f_regression, n_features=9)
    X = selector.fit_transform(X_reg, y_reg)
    assert X.shape[1] == 9
    assert list(selector.get_feature_names_out()) == list(X.columns)


def test_pca_strategy():
    """Assert that the pca strategy works as intended."""
    selector = FeatureSelector(strategy="pca", n_features=0.7)
    X = selector.fit_transform(X_bin)
    assert X.shape[1] == 21
    assert selector.pca_.get_params()["svd_solver"] == "auto"
    assert list(selector.get_feature_names_out()) == list(X.columns)


def test_pca_components():
    """Assert that the pca strategy creates components instead of features."""
    selector = FeatureSelector(strategy="pca", solver="arpack", n_features=5)
    X = selector.fit_transform(X_bin)
    assert selector.pca_.svd_solver == "arpack"
    assert "pca0" in X.columns


def test_pca_sparse_data():
    """Assert that the pca strategy uses TruncatedSVD for sparse data."""
    selector = FeatureSelector(strategy="pca", n_features=2)
    selector.fit(X_sparse)
    assert selector.pca_.__class__.__name__ == "TruncatedSVD"
    assert selector.pca_.get_params()["algorithm"] == "randomized"


def test_sfm_prefit_invalid_estimator():
    """Assert that an error is raised for an invalid estimator in sfm."""
    selector = FeatureSelector(
        strategy="sfm",
        solver=DecisionTreeClassifier(random_state=1).fit(X_class, y_class),
        n_features=8,
        random_state=1,
    )
    with pytest.raises(ValueError, match=".*different columns than X.*"):
        selector.fit(X_bin, y_bin)


def test_sfm_strategy_not_threshold():
    """Assert that if threshold is not specified, sfm selects n_features features."""
    selector = FeatureSelector(
        strategy="sfm",
        solver=DecisionTreeClassifier(random_state=1),
        n_features=16,
        random_state=1,
    )
    X = selector.fit_transform(X_bin, y_bin)
    assert X.shape[1] == 16
    assert list(selector.get_feature_names_out()) == list(X.columns)


def test_sfm_strategy_fitted_solver():
    """Assert that the sfm strategy works when the solver is already fitted."""
    selector = FeatureSelector(
        strategy="sfm",
        solver=DecisionTreeClassifier(random_state=1).fit(X_bin, y_bin),
        n_features=7,
        random_state=1,
    )
    X = selector.fit_transform(X_bin)
    assert X.shape[1] == 7


def test_sfm_strategy_not_fitted_solver():
    """Assert that the sfm strategy works when the solver is not fitted."""
    selector = FeatureSelector(
        strategy="sfm",
        solver=DecisionTreeClassifier(random_state=1),
        n_features=5,
    )
    X = selector.fit_transform(X_bin, y_bin)
    assert X.shape[1] == 5


def test_sfs_strategy():
    """Assert that the sfs strategy works."""
    selector = FeatureSelector(
        strategy="sfs",
        solver="Tree_reg",
        n_features=6,
        cv=2,
        scoring="mae",
        random_state=1,
    )
    X = selector.fit_transform(X_reg, y_reg)
    assert X.shape[1] == 6
    assert list(selector.get_feature_names_out()) == list(X.columns)


def test_rfe_strategy():
    """Assert that the RFE strategy works as intended."""
    selector = FeatureSelector(
        strategy="rfe",
        solver=DecisionTreeClassifier(random_state=1),
        n_features=28,
        random_state=1,
    )
    X = selector.fit_transform(X_bin, y_bin)
    assert X.shape[1] == 28


def test_rfecv_strategy_before_pipeline_classification():
    """Assert that the rfecv strategy works before a fitted pipeline."""
    selector = FeatureSelector(
        strategy="rfecv",
        solver="Tree_class",
        n_features=None,
        cv=2,
        random_state=1,
    )
    X = selector.fit_transform(X_bin, y_bin)
    assert X.shape[1] == 3
    assert list(selector.get_feature_names_out()) == list(X.columns)


def test_rfecv_strategy_before_pipeline_regression():
    """Assert that the rfecv strategy works before a fitted pipeline."""
    selector = FeatureSelector(
        strategy="rfecv",
        solver="Tree_reg",
        n_features=16,
        cv=2,
        random_state=1,
    )
    X = selector.fit_transform(X_reg, y_reg)
    assert X.shape[1] == 10
    assert list(selector.get_feature_names_out()) == list(X.columns)


def test_kwargs_parameter_threshold():
    """Assert that the kwargs parameter works as intended."""
    selector = FeatureSelector(
        strategy="sfm",
        solver=DecisionTreeClassifier,
        n_features=3,
        threshold="mean",
        random_state=1,
    )
    X = selector.fit_transform(X_bin, y_bin)
    assert X.shape[1] == 3


def test_kwargs_parameter_pca():
    """Assert that custom kwargs can be provided to pca."""
    selector = FeatureSelector(
        strategy="pca",
        solver="arpack",
        tol=0.001,
        n_features=12,
        max_repeated=None,
        max_correlation=None,
        random_state=1,
    )
    X = selector.fit_transform(X_bin)
    assert X.shape[1] == 12


def test_advanced_no_get_feature_names_out():
    """Assert that get_feature_names_out is not implemented for advanced strats."""
    selector = FeatureSelector(
        strategy="pso",
        solver="tree_class",
        n_iteration=1,
        population_size=1,
    ).fit(X_bin, y_bin)
    with pytest.raises(NotImplementedError, match=".*get_feature_names_out.*"):
        selector.get_feature_names_out()


def test_advanced_provided_validation_sets():
    """Assert that custom validation sets can be provided."""
    selector = FeatureSelector(
        strategy="pso",
        solver="tree_class",
        X_valid=X_bin.iloc[:20, :],
        y_valid=y_bin.iloc[:20],
        n_iteration=2,
        population_size=2,
    )
    X = selector.fit_transform(X_bin, y_bin)
    assert X.shape[1] < X_bin.shape[1]


def test_advanced_missing_y_valid():
    """Assert that an error is raised when y_valid is missing."""
    selector = FeatureSelector("pso", solver="tree_class", X_valid=X_bin)
    with pytest.raises(ValueError, match=".*y_valid parameter.*"):
        selector.fit(X_bin, y_bin)


def test_advanced_custom_scoring():
    """Assert that the user can specify a custom scorer."""
    selector = FeatureSelector(
        strategy="pso",
        solver="tree_class",
        n_iteration=1,
        population_size=1,
        scoring="auc",
    )
    selector = selector.fit(X_bin, y_bin)
    assert selector.pso_.kwargs["scoring"].name == "auc"


def test_advanced_binary_classification_scoring():
    """Assert that scoring is set for binary classification tasks."""
    selector = FeatureSelector(
        strategy="pso",
        solver="tree_class",
        n_iteration=1,
        population_size=1,
    )
    selector = selector.fit(X_bin, y_bin)
    assert selector.pso_.kwargs["scoring"].name == "f1"


def test_advanced_multiclass_classification_scoring():
    """Assert that scoring is set for multiclass classification tasks."""
    selector = FeatureSelector(
        strategy="pso",
        solver="tree_class",
        n_iteration=1,
        population_size=1,
    )
    selector = selector.fit(X_class, y_class)
    assert selector.pso_.kwargs["scoring"].name == "f1_weighted"


def test_advanced_regression_scoring():
    """Assert that scoring is set for regression tasks."""
    selector = FeatureSelector(
        strategy="hho",
        solver="tree_reg",
        n_iteration=1,
        population_size=1,
    )
    selector = selector.fit(X_reg, y_reg)
    assert selector.hho_.kwargs["scoring"].name == "r2"


def test_advanced_custom_objective_function():
    """Assert that a custom objective function can be used."""
    selector = FeatureSelector(
        strategy="gwo",
        solver="tree_class",
        objective_function=lambda *args: 1,  # noqa: ARG005
        n_iteration=1,
        population_size=1,
    )
    selector = selector.fit(X_bin, y_bin)
    assert selector.gwo_.objective_function.__name__ == "<lambda>"
