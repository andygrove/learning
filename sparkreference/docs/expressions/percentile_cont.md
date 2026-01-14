# PercentileCont

## Overview
PercentileCont calculates a percentile value based on a continuous distribution of numeric or ANSI interval columns at a given percentage. It implements the SQL PERCENTILE_CONT function which uses linear interpolation between values when the exact percentile position falls between two data points. This expression is a runtime-replaceable aggregate that delegates to the internal Percentile implementation.

## Syntax
```sql
PERCENTILE_CONT(percentage) WITHIN GROUP (ORDER BY column [ASC|DESC])
```

```scala
// Used internally by Catalyst - not directly exposed in DataFrame API
// The DataFrame API uses percentile_approx for similar functionality
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| left | Expression | The column expression to calculate percentile over (ORDER BY clause) |
| right | Expression | The percentile value between 0.0 and 1.0 |
| reverse | Boolean | Whether to reverse the ordering (DESC vs ASC), defaults to false |

## Return Type
Returns the same data type as the input column being aggregated (numeric types or ANSI interval types).

## Supported Data Types
Supports numeric data types and ANSI interval types as determined by the underlying Percentile implementation's input type validation.

## Algorithm

- Delegates computation to the internal Percentile class implementation
- Uses continuous distribution methodology with linear interpolation between adjacent values
- Processes data according to the specified ordering (ascending or descending)
- Validates that the percentile value is between 0.0 and 1.0
- Requires exactly one ordering expression in the WITHIN GROUP clause

## Partitioning Behavior
As an aggregate function, PercentileCont affects partitioning behavior:

- Requires data shuffle to collect all values for accurate percentile calculation
- Does not preserve input partitioning due to its global aggregation nature
- Must process all rows together to determine the correct percentile value

## Edge Cases

- Null handling behavior is delegated to the underlying Percentile implementation
- Empty input datasets return null
- Percentile values outside 0.0-1.0 range cause validation errors
- Requires exactly one ordering column - throws QueryCompilationError for multiple orderings
- DISTINCT clause is not supported and will be ignored
- UnresolvedWithinGroup state indicates incomplete ordering specification

## Code Generation
This expression uses runtime replacement with the Percentile class, so code generation support depends on the underlying Percentile implementation. The PercentileCont wrapper itself does not directly participate in code generation.

## Examples
```sql
-- Calculate median (50th percentile) of salary
SELECT PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY salary) as median_salary
FROM employees;

-- Calculate 95th percentile in descending order
SELECT PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY response_time DESC) as p95_response
FROM requests;
```

```scala
// This is an internal Catalyst expression
// DataFrame API equivalent would use approxQuantile or percentile_approx
df.stat.approxQuantile("salary", Array(0.5), 0.0)
```

## See Also

- Percentile - The underlying implementation class
- PercentileDisc - Discrete percentile calculation
- RuntimeReplaceableAggregate - Base trait for replaceable aggregates
- SupportsOrderingWithinGroup - Interface for WITHIN GROUP syntax