"""DEPRECATED top-level utilities shim.

The real implementation now lives in `src.analysis.utils`. Importing
`src.utils` will raise an ImportError to encourage direct usage of the
new location.
"""

raise ImportError(
    "src.utils has been removed. Import from 'src.analysis.utils' instead. "
    "Example: from src.analysis.utils import normalize_window"
)
