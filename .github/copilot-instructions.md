# Copilot Instructions - Auto-Applied to All Requests

## CRITICAL: Always Follow These Rules

### When Creating/Modifying Code:
1. ✅ Add type hints to all functions
2. ✅ Add docstrings with Args, Returns, Raises, and Examples
3. ✅ Break functions >30 lines into helper functions
4. ✅ Use config from `src.core.config` (never hardcode values)
5. ✅ Add logging for important operations using the logger

### When Adding Dependencies:
1. ✅ Update `pyproject.toml` dependencies list with version and comment
2. ✅ Update `docs/dependencies.md` with purpose and justification
3. ✅ Update `README.md` installation section if user-facing

### When Creating New Functions:
1. ✅ Add to `docs/api-reference.md` under correct module section
2. ✅ Create unit test in `tests/test_{module}.py`
3. ✅ Add usage example in docstring (doctest-compatible)

### When Modifying Files:
1. ✅ Update `docs/ai-changelog.md` with change summary
2. ✅ Update relevant documentation in `docs/`
3. ✅ Verify `README.md` is still accurate

### Documentation Standards:
- **API docs**: `docs/api-reference.md`
- **Architecture**: `docs/architecture.md`
- **Config options**: `docs/configuration.md`
- **Dependencies**: `docs/dependencies.md`
- **Changelog**: `docs/ai-changelog.md`

## Context Loading Strategy

### File Summaries for Token Efficiency
When providing context or understanding the codebase:
1. **First reference** `docs/file-summaries.md` for quick overviews of all files
2. **Only read full files** when you need implementation details or making changes
3. **Use summaries** to understand project structure before diving deep

**Token Savings**: Summaries reduce context from ~5000+ tokens to ~800 tokens (~85% reduction)

### When Creating New Code:
1. ✅ Create/update file summary in `docs/file-summaries.md`
2. ✅ Add to `docs/api-reference.md` under correct module
3. ✅ Update `docs/ai-changelog.md` with changes
4. ✅ Create unit tests in `tests/test_{module}.py`

### When Modifying Existing Code:
1. ✅ Update corresponding file summary if purpose/functions change
2. ✅ Update `docs/api-reference.md` if signatures change
3. ✅ Update `docs/ai-changelog.md` with changes

### File Summary Format:
```markdown
## filename.py
**Purpose**: Brief description of what this file does
**Functions**: function1(), function2()
**Classes**: ClassName (if any)
**Key Imports**: pandas, numpy, etc.
**Notes**: Any important implementation details
```

## Code Patterns to Follow

### Function Structure:
```python
def function_name(param: Type, optional_param: Type = default) -> ReturnType:
    """
    Brief one-line description of what the function does.
    
    More detailed explanation if needed. Explain the algorithm,
    business logic, or why this approach was chosen.
    
    Args:
        param: Description of parameter
        optional_param: Description with default behavior
        
    Returns:
        Description of return value and format
        
    Raises:
        ErrorType: When and why this error occurs
        
    Examples:
        >>> function_name(value)
        expected_output
        >>> function_name(value, optional_param=other)
        other_output
    """
    logger.info(f"Processing {param}")
    # Implementation
    return result
```

### Module Structure:
```python
"""
Module: src.module.submodule
Purpose: High-level description of what this module does
Dependencies: Key external libraries used (pandas, numpy, etc.)
Output: What this module produces or modifies

Key Concepts:
- Concept 1: Explanation relevant to understanding the code
- Concept 2: Business logic or domain knowledge
- Concept 3: Performance considerations or limitations

Example Usage:
    from src.module.submodule import main_function
    result = main_function(data)
"""
from typing import List, Dict, Optional, Tuple
import logging

from src.core.config import CONSTANT_NAME

logger = logging.getLogger(__name__)
```

### Complex Logic Comments:
Add AI-friendly comments explaining **why**, not **what**:

```python
# AI Context: We use log-linear regression because stock prices
# tend to grow exponentially over time. Linear regression on log(price)
# captures this pattern better than regression on raw prices.
# See: https://en.wikipedia.org/wiki/Log-linear_model
pred_price = log_linear_predict(window, x_pred)

# AI Context: Normalize to [0,1] range for consistent comparison across
# stocks with different price scales. 0=historical min, 1=historical max.
normalized = (price - min_price) / (max_price - min_price)
```

### TODO Comments for Future AI Improvements:
```python
# TODO(AI): This loop could be vectorized using pandas.rolling()
# Current: O(n*m) where n=symbols, m=days per symbol
# Optimal: O(n) using grouped rolling operations
# Priority: Medium (works fine for <100 symbols)
for symbol, group in df.groupby('Symbol'):
    # ...
```

## Default Behavior

### ALWAYS Update Documentation When You:
- Add/remove functions (→ update `docs/api-reference.md`)
- Change function signatures (→ update `docs/api-reference.md`)
- Add dependencies (→ update `docs/dependencies.md` and `pyproject.toml`)
- Modify config options (→ update `docs/configuration.md`)
- Change data flow (→ update `docs/architecture.md`)
- Make any code changes (→ update `docs/ai-changelog.md`)

### NEVER:
- ❌ Hardcode values (use `src.core.config` constants)
- ❌ Skip type hints on function parameters/returns
- ❌ Skip docstrings on public functions
- ❌ Create functions >30 lines without refactoring into helpers
- ❌ Add dependencies without documenting why they're needed
- ❌ Use `print()` instead of `logger.info/debug/warning/error()`
- ❌ Ignore existing code patterns in the project

## Testing Requirements

### For Every New Function:
1. Create unit test in `tests/test_{module}.py`
2. Test happy path (normal usage)
3. Test edge cases (empty inputs, boundary conditions)
4. Test error cases (invalid inputs, exceptions)
5. Add doctest examples in docstring if simple

### Test Structure:
```python
def test_function_name():
    """Test function_name with normal inputs."""
    result = function_name(valid_input)
    assert result == expected_output
    
def test_function_name_edge_case():
    """Test function_name with empty/boundary inputs."""
    result = function_name(edge_input)
    assert result == expected_edge_output
    
def test_function_name_raises_error():
    """Test function_name raises appropriate error."""
    with pytest.raises(ValueError):
        function_name(invalid_input)
```

## Code Quality Standards

### Naming Conventions:
- **Functions/variables**: `lowercase_with_underscores`
- **Classes**: `PascalCase`
- **Constants**: `UPPERCASE_WITH_UNDERSCORES`
- **Private**: `_leading_underscore`

### Type Hints:
```python
from typing import List, Dict, Optional, Tuple, Union
import pandas as pd
import numpy as np

def process_data(
    df: pd.DataFrame,
    symbols: List[str],
    window: int = 20,
    config: Optional[Dict[str, any]] = None
) -> Tuple[pd.DataFrame, Dict[str, float]]:
    """Always include type hints for clarity."""
    pass
```

### Error Handling:
```python
def safe_function(data: pd.DataFrame) -> pd.DataFrame:
    """Handle errors gracefully with informative messages."""
    if data.empty:
        logger.warning("Received empty DataFrame, returning empty result")
        return pd.DataFrame()
    
    try:
        result = risky_operation(data)
    except ValueError as e:
        logger.error(f"Invalid data format: {e}")
        raise ValueError(f"Cannot process data: {e}") from e
    
    return result
```

## Performance Considerations

### Prefer Vectorized Operations:
```python
# GOOD: Vectorized pandas operation
df['normalized'] = (df['price'] - df['price'].min()) / (df['price'].max() - df['price'].min())

# AVOID: Row-by-row iteration (unless necessary)
for i in range(len(df)):
    df.loc[i, 'normalized'] = calculate_single(df.loc[i, 'price'])
```

### Document Performance Characteristics:
```python
def compute_metrics():
    """
    Compute metrics for all stocks.
    
    Performance: ~2 seconds per symbol on average hardware.
    Memory: O(n*m) where n=symbols, m=days of history.
    """
    pass
```

## Domain Knowledge (Stock Strategy)

### Key Concepts:
- **Normalization**: Maps current price to [0,1] position within historical range
  - 0 = at historical minimum
  - 1 = at historical maximum
  - 0.5 = neutral (used when insufficient history)
  
- **Log-Linear Prediction**: Assumes exponential growth pattern
  - Performs linear regression on log(price)
  - Projects future price at specified horizon (PREDICT_DAYS)
  - Returns predicted_price / current_price ratio

- **Windows**: 
  - WINDOW_SHORT (20 days): Short-term trend analysis
  - WINDOW_LONG (200 days): Long-term trend analysis
  - PREDICT_DAYS (200 days): Forecast horizon

### Data Flow:
1. **Fetch**: Download stock prices via yfinance → `data/stock_prices.csv`
2. **Compute**: Calculate metrics from prices → `data/metrics.csv`
3. **Analyze**: Use metrics for stock selection/ranking

### Configuration:
All configurable values stored in `src/core/config.py`:
- Load from `config.yaml` if present
- Fall back to sensible defaults
- Never hardcode in business logic

---

*These instructions are automatically loaded by GitHub Copilot for every request.*
*Last updated: 2025-11-26*

## AI Collaboration Guidelines

### When AI Suggests Changes:
- Always explain the reasoning behind suggestions (e.g., "This vectorization improves performance from O(n*m) to O(n)")
- Provide before/after code diffs for clarity
- Ask for confirmation on breaking changes

### When Working with Multiple Files:
- Reference file summaries first, then read specific functions
- Use `docs/architecture.md` for understanding data flow before suggesting changes
- Update all related docs in a single response when possible

### Performance Monitoring:
- Include estimated token usage in responses
- Flag when full file reads are necessary vs. summary-sufficient

## Context Priority Levels

### Context Loading Hierarchy:
1. **Quick Overview**: `docs/file-summaries.md` + `README.md` (always first, <200 tokens)
2. **Module Deep Dive**: Full file + `docs/api-reference.md` section (<500 tokens)
3. **Implementation Details**: Specific functions/classes when modifying (<300 tokens)
4. **Full Context**: Only for complex refactoring or new modules (as needed)

**Token Budget**: Aim for <1000 tokens per response by using summaries strategically.

## AI Self-Review Checklist

### Before Suggesting Code Changes:
- [ ] Type hints on all functions?
- [ ] Docstring with Args/Returns/Raises/Examples?
- [ ] Function <30 lines (or broken into helpers)?
- [ ] Config used instead of hardcoding?
- [ ] Logging added for key operations?
- [ ] Dependencies documented if added?
- [ ] Tests created for new functions?
- [ ] Documentation updated (api-reference, changelog, summaries)?
- [ ] File summaries regenerated if code changed?

## Tool Integration

### VS Code Workflow:
- Use "Generate File Summaries" task after AI changes
- Run "Format Code" and "Lint Code" tasks before committing
- Use "Run Tests" to validate changes

### Git Workflow:
- Commit documentation updates separately from code changes
- Use descriptive commit messages following project patterns

### CI/CD Integration:
- Run summarizer in pipeline to keep docs current
- Execute tests automatically on pushes
- Lint and format checks in CI

## Instruction Maintenance

### Version Control:
- Update this file when project patterns change
- Include changelog at bottom for tracking improvements
- Review annually or when adding major features

### Changelog:
- **v1.0** (2025-11-26): Initial comprehensive instructions with file summaries
- **v1.1** (2025-11-26): Added collaboration guidelines, priority levels, and tool integration
