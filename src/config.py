"""DEPRECATED top-level shim.

This project has moved configuration into `src.core.config`. The top-level
`src.config` shim has been removed; importing it will raise an informative
ImportError to encourage direct usage of the new module.
"""

raise ImportError(
    "src.config has been removed. Import from 'src.core.config' instead. "
    "Example: from src.core.config import DATA_DIR"
)
