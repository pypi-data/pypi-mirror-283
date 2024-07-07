"""This module provides functions for flow cytometry-based mKeima assays.

By default, all functions expect dataframes with untransformed flow cytometry intensity
values, i.e. intensities must not be log transformed or binned. In FlowJo, this can be
achieved by exporting "scale" values from the workspace.

The following functions are available:

- `calculate_mkeima_ratio`: Adds "low pH mkeima" to "high pH mkeima" ratios to a
    dataframe.
- `calculate_mkeima_score`: Adds "low pH mkeima" to "high pH mkeima" scores to a
    dataframe. mKeima scores are log ratios of low pH to high pH mKeima signals,
    normalized to a reference sample by calculating z-scores using the median and
    standard deviation of the reference sample.
- `summarize`: Calculates summary statistics (mean, median, std, and number of events).
- `summarize_outliers`: Calculates the amount of outliers for each condition and
    replicate. Outliers are defined as events with a value above the a certain
    percentile (by default 98.5%) of the reference population.
- `scale_to_reference`: Scales values of a summary dataframe to the mean value of one
    (max value) or two reference conditions (min and max values). Adds a new column
    to the dataframe containing the scaled values.
"""

from typing import Optional

import pandas as pd
import numpy as np


def calculate_mkeima_ratio(
    data: pd.DataFrame,
    high_ph: str,
    low_ph: str,
) -> None:
    """Adds "low pH mkeima" to "high pH mkeima" ratios.

    Args:
        data: Dataframe containing flow cytometry data. Intensities must correspond to
            untransformed values, i.e. values must not be log transformed or binned.
        high_ph: Column corresponding to the high pH mKeima channel.
        low_ph: Column corresponding to the low pH mKeima channel.
    """
    data["mkeima ratio"] = data[low_ph] / data[high_ph]


def calculate_mkeima_score(
    data: pd.DataFrame,
    high_ph: str,
    low_ph: str,
    reference: str,
    group_by: Optional[str] = None,
    log_transform: bool = True,
) -> None:
    """Adds normalized "low pH mkeima" to "high pH mkeima" scores.

    Mkeima scores are normalized log ratios of low pH to high pH mKeima signals and
    calculated as follows. Low pH mKeima signals are divided by high pH mKeima signals
    and the ratios are log transformed with base 2. Log ratios are then normalized to
    the reference condition by subtracting the median of the of the reference population
    and then dividing by the standard deviation of the reference population. Normalized
    log ratios are added to the dataframe column "mkeima score".

    Args:
        data: Dataframe containing flow cytometry data.
        high_ph: Column corresponding to the high pH mKeima channel.
        low_ph: Column corresponding to the low pH mKeima channel.
        reference: Reference condition used to normalize ratios of low pH to high pH
            ratios. Must correspond to a value in data["Condition"].
        group_by: Optional, if specified the dataframe is grouped by unique values of
            this column and each group is normalized independently to the reference
            condition.
        log_transform: Default True. If True, low pH and high pH values are log2
            transformed before calculating mkeima scores. Set to False when the used
            flow cytometry intensities are already in log-space or binned.
    """
    if reference not in data["Condition"].unique():
        raise KeyError(
            f'The reference condition "{reference}" is not '
            f'present in data["Condition"]!'
        )

    if log_transform:
        data["mkeima score"] = np.log2(data[low_ph]) - np.log2(data[high_ph])
    else:
        data["mkeima score"] = data[low_ph] - data[high_ph]

    group_masks = []
    if group_by is not None:
        for group_name in data[group_by].unique():
            group_masks.append(data[group_by] == group_name)
    else:
        group_masks.append(np.ones(data.shape[0], dtype=bool))

    for group_mask in group_masks:
        group_data = data.loc[group_mask]

        norm_data = group_data.loc[(group_data["Condition"] == reference)]
        norm_median = np.median(norm_data["mkeima score"])
        norm_std = np.std(norm_data["mkeima score"])

        mkeima_scores = (group_data["mkeima score"] - norm_median) / norm_std
        mkeima_scores = mkeima_scores
        data.loc[group_mask, "mkeima score"] = mkeima_scores


def scale_to_reference(
    data: pd.DataFrame,
    on: str,
    reference: str,
    min_reference: Optional[str] = None,
    reference_range: tuple[float, float] = (0, 1),
    group_by: Optional[str] = None,
) -> None:
    """Transform values by scaling them to the mean value of the reference condition.

    Adds a new column to the dataframe containing the scaled values. The new column is
    named "{on} scaled". The formula used for the scaling is:

    X_std = (X - X_reference_min) / (X_reference_max - X_reference_min)
    X_scaled = X_std * (reference_range[1] - reference_range[0]) + reference_range[0]

    Args:
        data: Dataframe containing data for scaling.
        on: Specifies column which values will be scaled.
        reference: Reference condition used to normalize values, must correspond to a
            value in data["Condition"]. The mean value of this condition is used as the
            'max' value.
        min_reference: Reference condition used to define the zero value. If specified,
            the mean value of this condition is used as the 'min' value, must
            correspond to a value in data["Condition"]. If not specified, the minimum
            value of the data is used as the zero value.
        group_by: Optional, if specified the dataframe is grouped by unique values of
            this column and each group is normalized independently to the reference
            condition. The 'group_by' column cannot be "Condition" as this column is
            used to define the reference condition.
    """
    if reference not in data["Condition"].unique():
        raise KeyError(
            f'The "reference" condition "{reference}" is not '
            f'present in data["Condition"]!'
        )
    if min_reference is not None and min_reference not in data["Condition"].unique():
        raise KeyError(
            f'The "min_reference condition" "{min_reference}" is not '
            f'present in data["Condition"]!'
        )
    if group_by == "Condition":
        raise ValueError('"group_by" cannot be "Condition".')

    if group_by is None:
        grouping = [(None, data)]
    else:
        grouping = data.groupby(group_by)

    group_results = []
    for _, group in grouping:
        reference_max = np.mean(group.loc[(group["Condition"] == reference), on])
        if min_reference is not None:
            reference_min = np.mean(
                group.loc[(group["Condition"] == min_reference), on]
            )
        else:
            reference_min = np.min(group[on])
        min_range, max_range = reference_range

        scaled_values = (group[on] - reference_min) / (reference_max - reference_min)
        scaled_values = scaled_values * (max_range - min_range) + min_range
        group[f"{on} scaled"] = scaled_values
        group_results.append(group)
    results_table = pd.concat(group_results, ignore_index=True)
    return results_table


def summarize(
    data: pd.DataFrame,
    group_by: list[str] = ["Condition", "Replicate"],
    on: str = "mkeima score",
) -> pd.DataFrame:
    """Calculates summary statistics.

    Groups the data based on unique values in the specified columns and calculates
    the mean, standard deviation, and median of the column selected with the 'on'
    parameter, as wel as the total number of events.

    Args:
        data: Dataframe used for summarizing.
        group_by: Default ["Condition", "Replicate"]. List of dataframe columns that
            will be used for grouping data before summarizing each group individually.
            Should include all columns that are necessary to distinguish each unique
            sample.
        on: Default "mkeima score". Specifies column that will be used for summarizing.

    Returns:
        A dataframe containing the columns used for grouping, as well as "Median",
        "Mean", "Std", and "Total events".
    """
    results = (
        data.groupby(by=group_by)
        .agg(
            Median=(on, np.median),
            Mean=(on, np.mean),
            Std=(on, np.std),
            Events=(on, "size"),
        )
        .reset_index()
    )
    results.rename(columns={"Events": "Total events"}, inplace=True)
    return results


def summarize_outliers(
    data: pd.DataFrame,
    reference: str,
    on: str = "mkeima ratio",
    reference_percentile: float = 98.5,
    group_by: Optional[list] = None,
) -> pd.DataFrame:
    """Calculates the amount of outliers for each condition and replicate.

    The threshold for outliers is defined as the 98.5 percentile of the mkeima ratio
    distribution from the reference condition. Entries in the dataframe are grouped
    according to unique values in the "Condition" and "Replicate" columns, and for each
    group the number and relative amount of outliers is calculated.

    Args:
        data: Dataframe used for summarizing. Must contain the columns "Condition" and
        "Replicate", as well as columns specified by the 'on' and 'group_by' arguments.
        reference: Reference condition that is used for calculating an outlier
            threshold. Must correspond to a value in data["Condition"].
        on: Default "mkeima ratio". Specifies column that will be used for calculating
            the number of outliers.
        reference_percentile: Percentile of the reference condition to calculate the
            threshold that defines outliers. Default is 98.5.
        group_by: Optional, list of dataframe columns. If specified, the dataframe is
            first grouped by unique values of these columns and the outlier threshold
            and outliers are calculated for each group separately.

    Returns:
        A dataframe containing the columns "Condition", "Replicate", "Total events",
        "Outliers", "Outliers [%]", and the columns specified by the 'group_by'
        argument.
    """
    default_grouping = ["Condition", "Replicate"]
    if group_by is not None:
        group_by = [by for by in group_by if by not in default_grouping]
        if not group_by:
            group_by = None

    if group_by is None:
        grouping = [(None, data)]
    else:
        grouping = data.groupby(group_by)

    group_results = []
    for group_name, group_data in grouping:
        reference_mask = group_data["Condition"] == reference
        reference_scores = group_data.loc[reference_mask, on]
        cutoff_uppers = np.percentile(reference_scores, reference_percentile)

        results = (
            group_data.groupby(by=default_grouping)
            .agg(
                Events=(on, "size"),
                Outliers=(on, lambda x: (x >= cutoff_uppers).sum()),
            )
            .reset_index()
        )
        results["Outliers [%]"] = (results["Outliers"] / results["Events"]) * 100
        results.rename(columns={"Events": "Total events"}, inplace=True)

        # Add columns from the user specified grouping
        if group_name is not None:
            if isinstance(group_name, str):
                group_name = (group_name,)
            for column_value, column in zip(group_name, group_by):
                results[column] = column_value
        group_results.append(results)
    results_table = pd.concat(group_results, ignore_index=True)
    return results_table
