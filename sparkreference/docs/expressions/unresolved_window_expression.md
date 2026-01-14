# UnresolvedWindowExpression

## Overview
UnresolvedWindowExpression is an intermediate expression used during Catalyst's analysis phase to represent window functions that have not yet been resolved with their specific window specifications. It serves as a placeholder that gets transformed into concrete window expressions during the resolution process.

## Syntax
This expression is not directly used in SQL or DataFrame API - it's an internal Catalyst representation created during parsing and analysis phases.

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| child | Expression | The window function expression to be applied |
| windowSpec | WindowSpecReference | Reference to the window specification defining partitioning, ordering, and frame bounds |

## Return Type
Cannot determine return type - throws `UnresolvedException` when `dataType` is accessed, as the actual data type depends on the resolved child expression.

## Supported Data Types
Not applicable - this expression cannot be evaluated and serves only as a placeholder during analysis. The supported data types depend on the underlying child expression after resolution.

## Algorithm
- Acts as a wrapper around an unresolved window function during Catalyst analysis
- Maintains reference to both the function expression and window specification
- Throws `UnresolvedException` for any evaluation-related operations
- Gets replaced by concrete window expressions during the resolution phase
- Implements `Unevaluable` trait to prevent direct evaluation attempts

## Partitioning Behavior
Not applicable during the unresolved state:
- Partitioning behavior depends on the resolved window expression
- Window specifications may define partitioning requirements
- Actual shuffle requirements determined after resolution

## Edge Cases
- **Evaluation attempts**: Throws `UnresolvedException` for `dataType` and `nullable` access
- **Resolution status**: Always returns `false` for `resolved` property
- **Analysis failures**: May cause analysis exceptions if window specification cannot be resolved
- **Invalid references**: Fails if `windowSpec` references non-existent window definitions

## Code Generation
Not applicable - this expression cannot generate code as it implements `Unevaluable`. Code generation occurs only after resolution into concrete window expressions.

## Examples
```sql
-- This SQL would create UnresolvedWindowExpression internally:
SELECT sum(value) OVER w FROM table
WINDOW w AS (PARTITION BY id ORDER BY timestamp)
```

```scala
// Internal representation (not user-facing):
UnresolvedWindowExpression(
  child = UnresolvedFunction("sum", Seq(col("value"))),
  windowSpec = WindowSpecReference("w")
)
```

## See Also
- `SpecifiedWindowFrame` - Concrete window frame specification
- `WindowExpression` - Resolved window expression
- `WindowSpecDefinition` - Complete window specification
- `UnaryExpression` - Parent expression type