"""Analysis of flow cytometry-based mKeima assays in Python."""

from .read import import_from_directory, import_facs_csv, infer_setup_from_filename
from .analyze import (
    calculate_mkeima_ratio,
    calculate_mkeima_score,
    scale_to_reference,
    summarize,
    summarize_outliers,
)


__version__ = "0.6.0"
