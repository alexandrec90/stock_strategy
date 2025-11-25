"""DEPRECATED top-level metrics shim.

The real implementation now lives in `src.analysis.metrics`. Importing
`src.metrics` will raise an ImportError to encourage direct usage of the
new location.
"""

raise ImportError(
    "src.metrics has been removed. Import from 'src.analysis.metrics' instead. "
    "Example: from src.analysis.metrics import compute_metrics"
)
