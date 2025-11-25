"""DEPRECATED top-level fetch_shim.

The data fetch implementation now lives in `src.data.fetch_stocks`. Importing
`src.fetch_stocks` will raise an ImportError to encourage direct usage of the
new module.
"""

raise ImportError(
    "src.fetch_stocks has been removed. Import from 'src.data.fetch_stocks' instead. "
    "Example: from src.data.fetch_stocks import main"
)