# AtLeastNNonNulls

## Overview
AtLeastNNonNulls is a predicate expression that evaluates to true if there are at least `n` non-null and non-NaN values among its child expressions. It performs null-safe evaluation and treats NaN values in floating-point types (Double and Float) as invalid values that don't count toward the threshold.

## Syntax
```scala
// Internal Catalyst expression - typically used in query optimization
AtLeastNNonNulls(n: Int, children: Seq[Expression])
```

## Arguments
| Argument | Type | Description |
|----------|------|-------------|
| n | Int | The minimum number of non-null, non-NaN values required |
| children | Seq[Expression] | The sequence of expressions to evaluate |

## Return Type
Boolean - always non-nullable (returns true or false, never null)

## Supported Data Types
All Spark SQL data types are supported as input expressions:

- Numeric types (with special NaN handling for Float and Double)
- String types
- Date/Timestamp types
- Complex types (Array, Map, Struct)
- Binary types

## Algorithm

- Iterate through child expressions in order, evaluating each one
- For each non-null result, check if it's a Float/Double type and verify it's not NaN
- Increment counter for valid (non-null, non-NaN) values
- Short-circuit evaluation: stop as soon as the threshold `n` is reached
- Return true if the count of valid values is greater than or equal to `n`

## Partitioning Behavior
This expression does not affect partitioning:

- Preserves existing partitioning as it operates on individual rows
- Does not require shuffle operations
- Can be evaluated locally within each partition

## Edge Cases

- Null handling: Null values are excluded from the count
- NaN handling: Float.NaN and Double.NaN values are treated as invalid and excluded
- Empty input: If no child expressions are provided, returns true only if n ≤ 0
- Zero threshold: If n = 0, always returns true regardless of input values
- Threshold exceeds children: If n > children.length, can only return true if all children are non-null/non-NaN

## Code Generation
This expression supports Tungsten code generation with optimizations:

- Generates specialized code paths for Float/Double types vs other types
- Uses early termination logic in generated code
- Implements expression splitting for large numbers of child expressions
- Falls back to interpreted mode only if code generation fails

## Examples
```sql
-- This expression is typically used internally by the Catalyst optimizer
-- It may appear in query plans for operations like COALESCE or NULL-safe joins
```

```scala
// Example usage in Catalyst expression trees
val expr = AtLeastNNonNulls(2, Seq(col("a"), col("b"), col("c")))
// Returns true if at least 2 of the three columns have non-null values

// Example with floating-point NaN handling
val floatExpr = AtLeastNNonNulls(1, Seq(lit(Double.NaN), lit(1.0), lit(null)))
// Returns true because lit(1.0) is the one non-null, non-NaN value needed
```

## See Also

- IsNull / IsNotNull expressions for single-column null checking
- Coalesce expression for selecting first non-null value
- NaNvl expression for NaN handling in floating-point operations
- Greatest/Least expressions for multi-column comparisons